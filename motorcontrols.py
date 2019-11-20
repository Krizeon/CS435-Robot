from machine import Pin
from machine import I2C
from DCMotors import *
from get_distance import *

MAX_SPEED = 4095 #max speed that can be sent to the motors over PWM
LEFT_MOTOR = 0 #index that corresponds to the left motor on the board
RIGHT_MOTOR = 1 #index that corresponds to the right motor on the board
SCL = Pin(22, Pin.OUT) #scl pin on the ESP32 for I2C comm
SDA = Pin(23, Pin.OUT) #sda pin on the ESP32 for I2C comm
LED = Pin(13, Pin.OUT) #the red LED pin on the Feather board

#setup code
i2c = I2C(scl=SCL, sda=SDA)  # create I2C peripheral at frequency of 400kHz
i2c.init(scl=SCL, sda=SDA)
MOTOR = DCMotors(i2c)  # Motor object

def convert_speed_to_percent(percent):
    """
    :param percent: percentage of speed of motors, 1 - 100
    :return: a speed between 0 - 4095 for the DCMotors functions to understand
    """
    speed = MAX_SPEED // 100
    simple_speed = speed * percent
    return simple_speed

def forward(speed, motor=MOTOR):
    """
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (-1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (-1 * motor_speed)) #flip the direction of the right motor

def backward(speed, motor=MOTOR):
    """
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (1 * motor_speed))  # flip the direction of the right motor

def right(speed, motor=MOTOR):
    """
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (-1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (1 * motor_speed))


def left(speed, motor=MOTOR):
    """
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (-1 * motor_speed))

def brake(motor=MOTOR):
    """
    :param motor: a DCMotor object
    :return: n/a
    """
    motor.brake(0)
    motor.brake(1)
    motor.brake(2)
    motor.brake(3)

def autonomous_drive(motor=MOTOR):
    while True:
        distance = get_distance()
        while distance > 100 and distance != 0:
            forward(50)
            utime.sleep_ms(25)
            distance = get_distance()
        backward(50)
        utime.sleep_ms(500)
        right(50)
        utime.sleep_ms((2000))