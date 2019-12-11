# CS435 Embedded Systems Final Project: Two-wheel Drive WiFi Controlled Robot with Autonomous Capabilities
By Kevin Hernandez and Dylan Montagu


## Introduction

For our final project in our Embedded System's course, we were given the task of building a "hands-on, creative learning experience" - very much an opened ended assignment! The only restraint was that our project had to be unique (not copied directly from the web), and demonstrate the various skills and understandings of Embedded Systems we'd learned over the course of the semester. The tools at our disposal were the Adafruit Circuit Playground (an Arduino compatible microcontroller built on top of the ATmega32u4 Processor), the Adafruit HUZZAH32 (Arduino and MicroPython compatible microcontroller built on top of the ESP32 dual-core chip, with WiFi capabilities), as well as all the code we had written throughout the semester. 

We both agreed that we wanted to create some sort of wheeled robot - how could you not? It's the classic embedded systems project. However, we wanted to provide functionality above the typical base-line "programmed path" project. Continuing along that train of thought, we decided that we wanted to implement the ability to control the robot over WiFi, as well as creating an autonomous mode. With our features decided, the board that we would use was decided for us - the ESP32. We also take on the challenge of using Micropython for coding the microcontroller to take advantage of the many existing libraries online.

In figuring out what hardware we would need to create this project, we explored many of the 'robot packages' sold on [Adafruit's website](https://learn.adafruit.com). As we were working on a budget, we had to determine what peripherals did we absolutely need to buy and what we could create on our own. We had figured that half the fun of creating a robot was building it, so we ultimately decided that non-electornic items such as a chassis were not necessary to buy! We started with knowledge on using certain design tools such as a laser cutter to cut out sheets of hardboard and wood for our robot parts, so we weren't too intimidated to design something simple from scratch.

# Methods/Planning 
We began with writing out our project proposal and deciding how we wanted to build our ideal mini robot. On top of finding robot building guides on Adafruit and Sparkfun, Kevin also had prior robotics experience which he used in our advantage for designing a simple two wheel drive robot robot. A small, cheap robot the size of our hands could drive with a back-wheel drive with two free-spinning wheels in the front. When turning, our robot should turn in place by spinning the left and right motors in opposite directions while the front wheels (which should be a slippery material such as wood) slide across the ground. In order for this to work properly, the back wheels would need to have a higher friction surface such as rubber from a rubber band to be able to turn in place. As far as electronics go, we found out that the Feather HUZZAH board could not drive motors directly from the digital pins, so we would need a motor driver attachment to power the motors. We also needed some kind of distance sensor that would be attached to the front of the robot for autonomous driving capabilities. 

Awesome! We planned out the ideas necessary to build a driving robot. So we set out to find the necessary parts on Adafruit's website, such as AA batteries, DC Servo motors (which Adafruit stated was ideal for small robots), LiPo battery packs, a Featherwing DC motor driver, and a distance sensor. We ordered these peripherals and set out to slowly figure out how to wire our robot together. There was lots of trial and error occuring when trying to connect the motors, but luckily no electronic was harmed in the process! During this process, we were designing and lasercutting our robot parts, which were largely inspired by this chassis design:

![Adafruit ESP8266 Mobile Robot](https://cdn-learn.adafruit.com/assets/assets/000/034/447/large1024/microcontrollers_hw5.jpg?1469777542)
https://learn.adafruit.com/build-an-esp8266-mobile-robot

We used Adobe Illustrator to design the parts that were to be lasercut and used CorelDRAW for any additional tweaks after multiple lasercutting trials. Lots of creative liberty was used in creating the parts, thus the design was finalized on the go. If this had been a more complex robot, use of CAD (computer-aided design) software for modeling the chassis would have been necessary. We did not feel the need to do this for this project as we wanted to put enough energy on the Embedded Systems aspect of the robot, too.

Since we were already stretching ourselves thin with various extra tasks in the process of making this project come to life, we decided to find existing Micropython libraries that could communicate with the Featherwing directly to drive the motors with ease. We found [this Micropython library](https://github.com/adafruit/micropython-adafruit-pca9685/) that was able to communicate with the Featherwing's onboard PCA9685 chip over 1^2C, a chip with PWM channels that is directly wired to the motor driving chips. We integrated the [pca9685.py](https://github.com/adafruit/micropython-adafruit-pca9685/blob/master/pca9685.py) and [motor.py](https://github.com/adafruit/micropython-adafruit-pca9685/blob/master/motor.py) files and modified them slightly to get them fully compatible with the ESP32's onboard libraries. This was mostly just changing the pca9685's use of the "time" library to "utime"  instead.

Once we got these files compatible and all wires were connected and soldered properly, we created our own [motor controlling drivers](https://github.com/Krizeon/CS435-Robot/blob/master/motorcontrols.py) that calls the functions from motor.py to forward, backwards, turn left and turn right functions for our robot. These functions control motors that are connecte to the M1 and M2 channels of the Featherwing. 

The task division fell into place naturally: Kevin wanted to design and build the robot parts, Dylan wanted to implement a wifi-communication system with the ESP32 and design a website with buttons for controlling the device. 



# References
https://www.geeksforgeeks.org/python-bytearray-function/
https://forum.micropython.org/viewtopic.php?t=762
https://docs.espressif.com/projects/esp-idf/en/latest/esp32s2beta.html
https://docs.micropython.org/en/latest/library/_thread.html
https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/thread
http://acoptex.com/project/2789/basics-project-076e-esp32-development-board-micropython-web-server-at-acoptexcom/#sthash.jI4TOzgE.dpbs
https://github.com/Krizeon/CS435-Robot/blob/master/README.md
https://www.sltrib.com/news/2019/08/19/yelling-siri-or-alexa/

