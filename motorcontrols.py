from machine import Pin
from machine import I2C
from DCMotors import *
from get_distance import *

MAX_SPEED = 4095  # max speed that can be sent to the motors over PWM
LEFT_MOTOR = 0  # index that corresponds to the left motor on the board
RIGHT_MOTOR = 1  # index that corresponds to the right motor on the board
SCL = Pin(22, Pin.OUT)  # scl pin on the ESP32 for I2C comm
SDA = Pin(23, Pin.OUT)  # sda pin on the ESP32 for I2C comm
LED = Pin(13, Pin.OUT)  # the red LED pin on the Feather board


# setup code
is_autonomous = False
i2c = I2C(scl=SCL, sda=SDA)  # create I2C peripheral at frequency of 400kHz
i2c.init(scl=SCL, sda=SDA) # initialize I2C communication
MOTOR = DCMotors(i2c) # create DCMotors object


def convert_speed_to_percent(percent):
    """
    Converts the 12-bit value of the DC motor speed to a percentage of 1-100.
    This is done to make the functions easier to use as we don't need a high
    resolution for motor speed.
    :param percent: percentage of speed of motors, 1 - 100
    :return: a speed between 0 - 4095 for the DCMotors functions to understand
    """
    # MAX_SPEED = 4095 (12-bit channel value)
    speed = MAX_SPEED // 100
    simple_speed = speed * percent
    return simple_speed


def forward(speed, motor=MOTOR):
    """
    Controls the robot to go forward
    When called, breaks the is_autonomous thread
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    global is_autonomous
    is_autonomous = False # kill this thread if the robot is currently in autonomous mode
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (-1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (-1 * motor_speed))


def backward(speed, motor=MOTOR):
    """
    Controls the robot to go backwards
    When called, breaks the is_autonomous thread
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    global is_autonomous
    is_autonomous = False # kill this thread if the robot is currently in autonomous mode
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (1 * motor_speed))


def right(speed, motor=MOTOR):
    """
    Controls the robot to turn right in place
    When called, breaks the is_autonomous thread
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    global is_autonomous
    is_autonomous = False # kill this thread if the robot is currently in autonomous mode
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (-1 * motor_speed)) # turn left wheel forwards
    motor.speed(RIGHT_MOTOR, (1 * motor_speed)) # turn right weel backwards


def left(speed, motor=MOTOR):
    """
    Controls the robot to turn left in place
    When called, breaks the is_autonomous thread
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    global is_autonomous
    is_autonomous = False # kill this thread if the robot is currently in autonomous mode
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (1 * motor_speed)) # turn left wheel backwards
    motor.speed(RIGHT_MOTOR, (-1 * motor_speed)) #turn right wheel forwards


def brake(motor=MOTOR):
    """
    Brings all motors to a halt
    When called, breaks the is_autonomous thread
    :param motor: a DCMotor object
    :return: n/a
    """
    global is_autonomous
    is_autonomous = False # kill this thread if the robot is currently in autonomous mode
    motor.brake(0)
    motor.brake(1)
    motor.brake(2)
    motor.brake(3)


def forward_autonomous(speed, motor=MOTOR):
    """
    Controls robot to go forward! This special version of movement is specific
    to autonomous mode, as it does not kill the autonomous thread.
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    motor_speed = convert_speed_to_percent(speed) # convert a percentage to a PWM speed
    motor.speed(LEFT_MOTOR, (-1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (-1 * motor_speed))


def backward_autonomous(speed, motor=MOTOR):
    """
    Controls robot to go backward! This special version of movement is specific
    to autonomous mode, as it does not kill the autonomous thread.
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (1 * motor_speed))


def right_autonomous(speed, motor=MOTOR):
    """
    Controls robot to turn right in place! This special version of movement is specific
    to autonomous mode, as it does not kill the autonomous thread.
    :param speed: a speed between 0 to 100
    :param motor: a DCMotor object
    :return: N/A (motors driving forward)
    """
    motor_speed = convert_speed_to_percent(speed)
    motor.speed(LEFT_MOTOR, (-1 * motor_speed))
    motor.speed(RIGHT_MOTOR, (1 * motor_speed))


def autonomous_drive(motor=MOTOR):
    """
    A basic autonomous mode that drives robot forward until it
    sees an object 100mm away from it, then turns right and continues
    :param motor: a DCMotor object
    :return: N/A (stops autonomous mode)
    """
    global is_autonomous
    is_autonomous = True
    while is_autonomous:
        distance = get_distance() # get the current distance to the nearest object, read by the distance sensor

        # if the distance sensor is over 4.5 meters away from an object, then the distance
        # sensor may read 0 occasionally (out of range). Therefore, we must check for false readings.
        if (distance > 100) or (distance == 0):
            forward_autonomous(50) # call forward without breaking autonomous thread
            utime.sleep_ms(25)  # move for 25 milliseconds before checking again for distance
        else:
            right_autonomous(50) # call right without breaking autonomous thread
            utime.sleep_ms(1000) # turn right for one second
    return
