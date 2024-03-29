"""
from https://github.com/adafruit/micropython-adafruit-pca9685/ (unedited)
Powers DC motors by giving a PWM signal over I2C to the onboard PCA9685 chip
on the Featherwing board. The I2C address is 0x60. PWM signal is a 12-bit
value (0-4095).
"""

from PCA9685 import *
_DC_MOTORS = ((8, 9, 10), (13, 12, 11), (2, 3, 4), (7, 6, 5))

class DCMotors:
    def __init__(self, i2c, address=0x60, freq=1600):
        self.pca9685 = PCA9685(i2c, address)
        self.pca9685.freq(freq)

    def _pin(self, pin, value=None):
        if value is None:
            return bool(self.pca9685.pwm(pin)[0])
        if value:
            self.pca9685.pwm(pin, 4096, 0)
        else:
            self.pca9685.pwm(pin, 0, 0)

    def speed(self, index, value=None):
        pwm, in2, in1 = _DC_MOTORS[index]
        if value is None:
            value = self.pca9685.duty(pwm)
            if self._pin(in2) and not self._pin(in1):
                value = -value
            return value
        if value > 0:
            # Forward
            self._pin(in2, False)
            self._pin(in1, True)
        elif value < 0:
            # Backward
            self._pin(in1, False)
            self._pin(in2, True)
        else:
            # Release
            self._pin(in1, False)
            self._pin(in2, False)
        self.pca9685.duty(pwm, abs(value))

    def brake(self, index):
        pwm, in2, in1 = _DC_MOTORS[index]
        self._pin(in1, True)
        self._pin(in2, True)
        self.pca9685.duty(pwm, 0)
