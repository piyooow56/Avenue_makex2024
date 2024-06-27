import novapi
import time
import math
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild import power_manage_module

# Config
Speed_Modifier = 2.5
TURN_SPEED_MODIFIER = 1.5

FR_ENCODE_M1 = encoder_motor_class("M1", "INDEX1")
FL_ENCODE_M2 = encoder_motor_class("M2", "INDEX1")
BR_ENCODE_M3 = encoder_motor_class("M3", "INDEX1")
BL_ENCODE_M4 = encoder_motor_class("M4", "INDEX1")

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

#run once
FR_ENCODE_M1.set_power(0)
BR_ENCODE_M3.set_power(0)
FL_ENCODE_M2.set_power(0)
BL_ENCODE_M4.set_power(0)

ENCODE_M5 = encoder_motor_class("M5", "INDEX1")
ENCODE_M6 = encoder_motor_class("M6", "INDEX1")

while True:
    if power_manage_module.is_auto_mode(): 
      pass
    else: 
        Movement()

        if gamepad.is_key_pressed("R1"):
            ENCODE_M5.set_power(80)
            ENCODE_M6.set_power(80)
        elif gamepad.is_key_pressed("R2"):
            ENCODE_M5.set_power(0)
            ENCODE_M6.set_power(0)
        elif gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("BL2",80)
        elif gamepad.is_key_pressed("L2"):
            power_expand_board.stop("BL2")
        elif gamepad.is_key_pressed("N1"):
            power_expand_board.set_power("DC1",100)
        elif gamepad.is_key_pressed("N2"):
            power_expand_board.set_power("DC1",-100)
        elif gamepad.is_key_pressed("N3"):
            power_expand_board.stop("DC3")


    pass