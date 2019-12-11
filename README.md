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


##### Bill of Materials
  * Adafruit Huzzah32: $19.95
  * US-100 Ultrasonic Distance Sensor: $6.95
  * DC Motor + Stepper FeatherWing: $21.50
  * DC Motor: $3.50 x 2 = $7.00
  * Lithium Ion Polymer Battery 3.7v 1200m: $9.95
  * 4 x AA Battery Holder: $2.95

##### Total Project Cost: $68.3





# Results

[![VIDEO](http://img.youtube.com/vi/MpUsSLf8D8k/0.jpg)](http://www.youtube.com/watch?v=MpUsSLf8D8k)

Demonstration Video


# Future Work
Overall, we're very happy with how our project turned out! It was a fantastic experience having to go through the research, trial, and troubleshooting phases of building an embedded system project. However, some aspects of our project that we'd like to improve are the autonomous mode, turning, user interface, and robot construction. 

Autonomous Mode: Our current implementation of autonomous mode is pretty simplistic - it boils down to "go forward, and turn right if an obstacle appears in front of the robot." This was adequate for our project, as the focus of this build wasn’t the autonomous mode, but rather the wholstic creation and implementation of an embedded system. As it was, our autonomous mode worked to ensure that our various peripherals (motors, distance sensor) were working correctly, and was fun to watch as it maneuvered throughout our classroom. However, creating a more thorough and robust autonomous would be the logical upgrade to our project. Having our robot able to make its way from point A to point B using various searching algorithms would be a fun project, especially now that we have a physical robot we can use to test with. This would likely require adding more sensors to our robot, as our current implementation with a single sensor will not register objects except those directly in front of it, causing it to occasionally run into objects it’s not perpendicular to. Utilizing 2 or 3 distance sensors would give us more information to work with when developing an autonomous mode program, and ultimately enhance the type of algorithms we could use. 

In a similar vein of thought, another aspect of the autonomous mode that we’d like to improve is how the distance sensor readouts are used. Currently, the autonomous reads the distance from the distance sensor every 50ms. While this is adequate for the current speeds our robot moves at and the distance thresholds we’ve set, a more elegant solution would be to connect the sensor to an ISR or run it in a new thread. In a multithreading scenario, we would have the get_distance thread send a signal to the main thread, which would handle the signal by stopping the robot, maneuvering the robot to a position in which it would no longer crash, then hand the reins back to the default autonomous mode. This implementation could also be made useful in regular user-control modes, where the would automatically stop the robot if it ever thought it was about to crash, regardless of the user’s input. 

# Turning
Our current implementation for turning is done by turning the rear wheels connected to the DC motors in opposite directions. For example, to turn left, the rear left wheel reverses, while the front right wheel goes forward. This results in the robot turning on the spot, but is overall not a fluid motion, especially since the front wheels are partially dragged in order to complete the tight turn. One improvement could be to create a turning method with a larger turning radius, similar to how a car would turn. This could be done by turning both powered wheels forward, but at different speeds. Another option could be using [mecanum wheels](https://www.andymark.com/products/4-in-hd-mecanum-wheel-set-options) which are able to turn and move sideways seamlessly, even without steering systems. 

# User Interface
The round-about method in which we created a WiFi control interface for our robot was due to the various network restrictions Middlebury College. As a result, there was a significant amount of control features that we would have liked to implement, but were unable to due to the limitations of the system we had to resort to using. With a more open network, we would have been able to implement a more interactive interface that allowed for more functionality beyond direction buttons and autonomous mode. Some simple improvements would be the addition of sliders next to the directional buttons to designate speed. Our motor driver functions take motor-speed as a parameter, however due to our web interface not being able to translate slider values back to the robot, we had to hardcode a motor speed into our functions despite the variable speed potential. 

If we were to completely rework our UI, something that we would like to focus is a mobile interface. Some big advantages of the touch screen functionality that provides would be virtual joystick controls, or even taking advantage of smart phone’s internal gyroscopes to provide controls by tilting the phone in various directions. 

# Robot Construction
In the time frame provided, we were able to make what is (in our opinion) a very sleek and well put together robot chassis. Kevin’s diligence on the laser cutter and soldering experience allowed us to have a very compact, yet functional final product. However, with more time on our hands, we would have likely decided to make more robust wheels with greater traction, a thicker distance sensor holder, and an encapsulating housing for our ESP32 and battery packs. 





# References
https://www.geeksforgeeks.org/python-bytearray-function/
https://forum.micropython.org/viewtopic.php?t=762
https://docs.espressif.com/projects/esp-idf/en/latest/esp32s2beta.html
https://docs.micropython.org/en/latest/library/_thread.html
https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/thread
http://acoptex.com/project/2789/basics-project-076e-esp32-development-board-micropython-web-server-at-acoptexcom/#sthash.jI4TOzgE.dpbs
https://github.com/Krizeon/CS435-Robot/blob/master/README.md
https://www.sltrib.com/news/2019/08/19/yelling-siri-or-alexa/


