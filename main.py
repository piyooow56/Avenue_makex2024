import novapi
import time
import math
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild import power_manage_module
from mbuild.ranging_sensor import ranging_sensor_class

# Config
Speed_Modifier = 2.5
TURN_SPEED_MODIFIER = 1.5

FR_ENCODE_M1 = encoder_motor_class("M1", "INDEX1")
FL_ENCODE_M2 = encoder_motor_class("M2", "INDEX1")
BR_ENCODE_M3 = encoder_motor_class("M3", "INDEX1")
BL_ENCODE_M4 = encoder_motor_class("M4", "INDEX1")
#Encode for Feed and servo
ENCODE_M5 = encoder_motor_class("M5", "INDEX1")
ENCODE_M6 = encoder_motor_class("M6", "INDEX1")
SMSERVO_M5 = smartservo_class("M5","INDEX1")


def Motor_RPM(M1, M2, M3, M4):
    FR_ENCODE_M1.set_speed(M1)
    FL_ENCODE_M2.set_speed(M2)
    BR_ENCODE_M3.set_speed(M3)
    BL_ENCODE_M4.set_speed(M4)

def Movement ():
    """Movement Code naja"""
    LYp = gamepad.get_joystick("Ly") * Speed_Modifier
    LYn = LYp * -1
    LXp = gamepad.get_joystick("Lx") * Speed_Modifier
    LXn = LXp * -1
    RXp = gamepad.get_joystick("Rx") * Speed_Modifier
    RXn = RXp * -1
    TURN_SPEED = RXn * TURN_SPEED_MODIFIER
    if LYp > 5 or LYp < -5:
        Motor_RPM(0, LYp, LYn, 0)
    elif LXp > 5 or LXp < -5:
        Motor_RPM(LXn, 0, 0, LXp)
    elif RXp > 5 or RXp < -5:
        Motor_RPM(TURN_SPEED, TURN_SPEED, TURN_SPEED, TURN_SPEED)
    else:
        Motor_RPM(0, 0, 0, 0)

def Auto_Turn(degree:int):
    """Turn Left or Right (+degree for Left, -degree for Right)"""
    target_angle = novapi.get_roll() + degree
    if target_angle > novapi.get_roll():
        while novapi.get_roll() < target_angle :
            Motor_RPM(100,100,100,100)
    elif target_angle < novapi.get_roll():
        while novapi.get_roll() > target_angle :
            Motor_RPM(-100,-100,-100,-100)
    Motor_RPM(0, 0, 0, 0)

#run once
FR_ENCODE_M1.set_power(0)
BR_ENCODE_M3.set_power(0)
FL_ENCODE_M2.set_power(0)
BL_ENCODE_M4.set_power(0)

FRanging = ranging_sensor_class("PORT3","INDEX1")
LRanging = ranging_sensor_class("PORT3","INDEX2")

def Auto1 ():
    
    while LRanging.get_distance() < 100 :
        Motor_RPM(100,0,0,100)
    Motor_RPM(0,0,0,0)
    ENCODE_M5.set_power(59)
    ENCODE_M6.set_power(59)
    while FRanging.get_distance() > 20 :
        Motor_RPM(0,100,100,0)
    Motor_RPM(0,0,0,0)
    ENCODE_M5.set_power(0)
    ENCODE_M6.set_power(0)
    Auto_Turn(50)
    for i in range(5):
        power_expand_board.set_power("BL1",80)
        time.sleep(0.1)
        power_expand_board.set_power("BL1",0)
        time.sleep(0.1)
    ENCODE_M5.set_power(59)
    ENCODE_M6.set_power(59)
    
def AutoManual():
    #slide left 100,-100,slide righ 100,-100
    Motor_RPM(100,0,0,-100)
    time.sleep(5) 
    Motor_RPM(0,0,0,0)
    ENCODE_M5.set_power(-40)
    ENCODE_M6.set_power(-40)
    Motor_RPM(0,100,-100,0)
    time.sleep(2)
    Motor_RPM(0,0,0,0)
    ENCODE_M5.set_power(0)
    ENCODE_M6.set_power(0)
    time.sleep(300)
    

while True:
    if power_manage_module.is_auto_mode(): 
      #AUTO
      AutoManual()
      pass
    else: 
        Movement()

        if gamepad.is_key_pressed("L1"):
            # Brushless on
            power_expand_board.set_power("BL1",80)
        elif gamepad.is_key_pressed("L2"):
            # Brushless off
            power_expand_board.stop("BL1")

        if gamepad.is_key_pressed("Up"):
            # Shooter Servo Up
            SMSERVO_M5.move_to(-50,20)
        elif gamepad.is_key_pressed("Down"):
            # Shooter Servo Down
            SMSERVO_M5.move_to(-95,20)

        if gamepad.is_key_pressed("R1"):
            # Feeed
            ENCODE_M5.set_power(-45)
            ENCODE_M6.set_power(-45)
        elif gamepad.is_key_pressed("R2"):
            # Reverse Feed
            ENCODE_M5.set_power(45)
            ENCODE_M6.set_power(45)
        else:
            ENCODE_M5.set_power(0)
            ENCODE_M6.set_power(0)

        if gamepad.is_key_pressed("N2"):
            # Gripper up
            power_expand_board.set_power("DC5",100)
        elif gamepad.is_key_pressed("N3"):
            # Gripper down
            power_expand_board.set_power("DC5",-100)
        else : 
            power_expand_board.set_power("DC5",5)

        if gamepad.is_key_pressed("N4"):
            # Gripper Close
            power_expand_board.set_power("DC6",80)
        elif gamepad.is_key_pressed("N1"):
            # Gripper Open
            power_expand_board.set_power("DC6",-80)
        else : 
            power_expand_board.set_power("DC6",0)

    pass