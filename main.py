import novapi
import time
import math
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild import power_manage_module

# Config
SPEED_MODIFIER = 250
TURN_SPEED_MODIFIER = 1.5
DEADZONE = 10
Mode = 1

#Movement Encode
FR_ENCODE_M1 = encoder_motor_class("M1", "INDEX1")
FL_ENCODE_M2 = encoder_motor_class("M2", "INDEX1")
BR_ENCODE_M3 = encoder_motor_class("M3", "INDEX1")
BL_ENCODE_M4 = encoder_motor_class("M4", "INDEX1")
#Encode for Feed and servo
ENCODE_M5 = encoder_motor_class("M5", "INDEX1")
ENCODE_M6 = encoder_motor_class("M6", "INDEX1")
SMSERVO_M5 = smartservo_class("M5","INDEX1")


def Motor_RPM(M1, M2, M3, M4):
    FR_ENCODE_M1.set_speed(round(M1))
    FL_ENCODE_M2.set_speed(round(M2))
    BR_ENCODE_M3.set_speed(round(M3))
    BL_ENCODE_M4.set_speed(round(M4))

def NormalAssDrive():
    LYp = (gamepad.get_joystick("Ly") / 100) * SPEED_MODIFIER
    LYn = LYp * -1
    LXp = (gamepad.get_joystick("Lx") / 100) * SPEED_MODIFIER
    LXn = LXp * -1
    RXp = gamepad.get_joystick("Rx") / 100
    RXn = RXp * -1
    TURN_SPEED = RXn * TURN_SPEED_MODIFIER
    if LYp > 5 or LYp < -5:
        Motor_RPM(LYn, LYn, LYp, LYp)
    elif LXp > 5 or LXp < -5:
        Motor_RPM(LXp, LXn, LXp, LXn)
    elif RXp > 5 or RXp < -5:
        Motor_RPM(TURN_SPEED, TURN_SPEED, TURN_SPEED, TURN_SPEED)
    else:
        Motor_RPM(0, 0, 0, 0)

def SemiHoloMecanum():
    """Movement Code naja"""
    LX = gamepad.get_joystick("Lx") 
    LY = gamepad.get_joystick("Ly") 
    RX = gamepad.get_joystick("Rx")

    if abs(LX) > 10 or abs(LY) > 10:
        arc = math.atan2(-LY, LX)
        cross_left_RPM = math.sin(arc + (1/4 * math.pi)) * SPEED_MODIFIER
        cross_right_RPM = math.sin(arc - (1/4 * math.pi)) * SPEED_MODIFIER
        Motor_RPM(cross_right_RPM, -cross_left_RPM, cross_left_RPM, -cross_right_RPM)
    elif abs(RX) > 10:
        TURN_SPEED = -RX * TURN_SPEED_MODIFIER
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

def Move_FB(rpm):
    """Move Forward and Backward (+rpm for Forward, -rpm for Backward)"""
    Motor_RPM(rpm * -1, rpm, rpm * -1, rpm)

def Move_LR(rpm):
    """Move Side Left and Right (+rpm for Left, -rpm for Right)"""
    Motor_RPM(rpm*-1, rpm*-1, rpm, rpm)

def Move_Diag(direction, rpm):
    """
    Moves the robot diagonally in the specified direction.  
    FL, FR, BL, BR  
    """
    if direction == "FL":
        Motor_RPM(0, rpm, -rpm, 0)
    elif direction == "FR":
       Motor_RPM(rpm, 0, 0, -rpm)
    elif direction == "BL":
       Motor_RPM(-rpm, 0, 0, rpm)
    elif direction == "BR":
        Motor_RPM(0, -rpm, rpm, 0)
    else:
        Motor_RPM(0,0,0,0)

def Move_Stop() :
    FR_ENCODE_M1.set_power(0)
    FL_ENCODE_M2.set_power(0)
    BR_ENCODE_M3.set_power(0)
    BL_ENCODE_M4.set_power(0) 
    FR_ENCODE_M1.set_speed(0)
    FL_ENCODE_M2.set_speed(0)
    BR_ENCODE_M3.set_speed(0)
    BL_ENCODE_M4.set_speed(0) 

def AutoManual():
    #Move left = 100 , Move Right = -100
    Move_LR(-100)
    time.sleep(1.8)
    Move_Stop()
    #Move forward = 100 , Move backward = -100
    Move_FB(75)
    ENCODE_M6.set_power(-60)
    ENCODE_M5.set_power(-60)
    power_expand_board.set_power("DC7",-80)
    power_expand_board.set_power("DC8",-80)
    time.sleep(3.8)
    Move_Stop()
    time.sleep(1)
    ENCODE_M6.set_power(0)
    ENCODE_M5.set_power(0)
    power_expand_board.set_power("DC7",0)
    power_expand_board.set_power("DC8",0)
    time.sleep(300)

def mode_normal():
    if gamepad.is_key_pressed("L1"):
            # Brushless on
        if SMSERVO_M5.get_value("voltage") < 12:
            power_expand_board.set_power("BL1",90)
        else:
            power_expand_board.set_power("BL1",80)
            
    elif gamepad.is_key_pressed("L2"):
        # Brushless off
        power_expand_board.stop("BL1")

    if gamepad.is_key_pressed("Up"):
        # Shooter Servo Up
        SMSERVO_M5.move_to(-35,20)
    elif gamepad.is_key_pressed("Down"):
        # Shooter Servo Down
        SMSERVO_M5.move_to(-110,20)
    elif gamepad.is_key_pressed("Left"):
        #Shooter Servo 
        SMSERVO_M5.move_to(-80,20)
    elif gamepad.is_key_pressed("Right"):
        #Shooter Servo 
        SMSERVO_M5.move_to(-90,20)

    if gamepad.is_key_pressed("R1"):
        # Feeed
        ENCODE_M5.set_power(-70)
        ENCODE_M6.set_power(-70)
        power_expand_board.set_power("DC7",-80)
        power_expand_board.set_power("DC8",-80)
    elif gamepad.is_key_pressed("R2"):
        # Reverse Feed
        ENCODE_M5.set_power(70)
        ENCODE_M6.set_power(70)
        power_expand_board.set_power("DC7",80)
        power_expand_board.set_power("DC8",80)

    else:
        ENCODE_M5.set_power(0)
        ENCODE_M6.set_power(0)
        power_expand_board.set_power("DC7",0)
        power_expand_board.set_power("DC8",0)

    if gamepad.is_key_pressed("N2"):
        # Gripper up
        power_expand_board.set_power("DC5",-100)
    elif gamepad.is_key_pressed("N3"):
        # Gripper down
        power_expand_board.set_power("DC5",100)
    else : 
        power_expand_board.set_power("DC5",-5)

    if gamepad.is_key_pressed("N1"):
        # Gripper Close
        power_expand_board.set_power("DC6",100)
    elif gamepad.is_key_pressed("N4"):
        # Gripper Open
        power_expand_board.set_power("DC6",-100)
    else : 
        power_expand_board.set_power("DC6",0)

def mode_Shootblock():
    if gamepad.is_key_pressed("L1"):
            # Brushless on
        if SMSERVO_M5.get_value("voltage") < 12:
            power_expand_board.set_power("BL1",90)
        else:
            power_expand_board.set_power("BL1",80)
            
    elif gamepad.is_key_pressed("L2"):
        # Brushless off
        power_expand_board.stop("BL1")
    
    if gamepad.is_key_pressed("R1"):
        # Feeed
        ENCODE_M5.set_power(-80)
        ENCODE_M6.set_power(-80)
        power_expand_board.set_power("DC7",-80)
        power_expand_board.set_power("DC8",-80)
    elif gamepad.is_key_pressed("R2"):
        # Reverse Feed
        ENCODE_M5.set_power(80)
        ENCODE_M6.set_power(80)
        power_expand_board.set_power("DC7",80)
        power_expand_board.set_power("DC8",80)
    else:
        ENCODE_M5.set_power(0)
        ENCODE_M6.set_power(0)
        power_expand_board.stop("DC7")
        power_expand_board.stop("DC8")
    
    if gamepad.is_key_pressed("N2"):
        SMSERVO_M5.move_to(-120,20)

#run once
FR_ENCODE_M1.set_power(0)
BR_ENCODE_M3.set_power(0)
FL_ENCODE_M2.set_power(0)
BL_ENCODE_M4.set_power(0)

while True:
    if power_manage_module.is_auto_mode(): 
      #AUTO
      pass
    else: 
        # Normal Drive (forward back left right)
        #NormalAssDrive()
        # Semi-Holomonic Drive (forward back left right diagonal)
        SemiHoloMecanum()
        # EXPERIMENTAL Holomonic Drive (forward back left right diagonal turn)
        # HolomonicMecanumV1()

        if gamepad.is_key_pressed("+") and gamepad.is_key_pressed("N1"):
            Mode = 1
        elif gamepad.is_key_pressed("+") and gamepad.is_key_pressed("N2"):
            Mode = 2
        elif gamepad.is_key_pressed("+") and gamepad.is_key_pressed("N3"):
            Mode = 3    

        if Mode == 1:
            mode_normal()
        elif Mode == 3:
            mode_Shootblock()
            
    pass