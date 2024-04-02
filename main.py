import novapi
import time
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild import power_manage_module

FR_ENCODE_M1 = encoder_motor_class("M1", "INDEX1")
BR_ENCODE_M2 = encoder_motor_class("M2", "INDEX1")
FL_ENCODE_M3 = encoder_motor_class("M3", "INDEX1")
BL_ENCODE_M4 = encoder_motor_class("M4", "INDEX1")

#run once
FR_ENCODE_M1.set_power(0)
BR_ENCODE_M2.set_power(0)
FL_ENCODE_M3.set_power(0)
BL_ENCODE_M4.set_power(0)

while True:
    # run forever
    if gamepad.get_joystick("Rx"):
        
    pass