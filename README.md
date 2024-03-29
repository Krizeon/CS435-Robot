# CS435 Embedded Systems Final Project: Two-wheel Drive WiFi Controlled Robot with Autonomous Capabilities
By Kevin Hernandez and Dylan Montagu

![robot picture](/images/robot_picture.png)


## Introduction

For our final project in our Embedded System's course, we were given the task of building a "hands-on, creative learning experience" - very much an open-ended assignment! The only restraint was that our project had to be unique (not copied directly from the web), and demonstrate the various skills and understandings of Embedded Systems we'd learned over the course of the semester. The tools at our disposal were the Adafruit Circuit Playground (an Arduino compatible microcontroller built on top of the ATmega32u4 Processor), the Adafruit HUZZAH32 (Arduino and MicroPython compatible microcontroller built on top of the ESP32 dual-core chip, with WiFi capabilities), as well as all the code we had written throughout the semester. 

We both agreed that we wanted to create some sort of wheeled robot - how could you not? It's the classic embedded systems project. However, we wanted to provide functionality above the typical base-line "programmed path" project. Continuing along that train of thought, we decided that we wanted to implement the ability to control the robot over WiFi, as well as creating an autonomous mode. With our features decided, the board that we would use was decided for us - the ESP32. We also take on the challenge of using Micropython for coding the microcontroller to take advantage of the many existing libraries online.

In figuring out what hardware we would need to create this project, we explored many of the 'robot packages' sold on [Adafruit's website](https://learn.adafruit.com). As we were working on a budget, we had to determine what peripherals did we absolutely need to buy and what we could create on our own. We had figured that half the fun of creating a robot was building it, so we ultimately decided that non-electronic items such as a chassis were not necessary to buy! We started with knowledge on using certain design tools such as a laser cutter to cut out sheets of hardboard and wood for our robot parts, so we weren't too intimidated to design something simple from scratch.



## Methods/Planning 

We began with writing out our project proposal and deciding how we wanted to build our ideal mini robot. On top of finding robot building guides on Adafruit and Sparkfun, Kevin also had prior robotics experience which he used in our advantage for designing a simple two wheel drive robot robot. A small, cheap robot the size of our hands could drive with a back-wheel drive with two free-spinning wheels in the front. When turning, our robot should turn in place by spinning the left and right motors in opposite directions while the front wheels (which should be a slippery material such as wood) slide across the ground. In order for this to work properly, the back wheels would need to have a higher friction surface such as rubber from a rubber band to be able to turn in place. As far as electronics go, we found out that the Feather HUZZAH board could not drive motors directly from the digital pins, so we would need a motor driver attachment to power the motors. We also needed some kind of distance sensor that would be attached to the front of the robot for autonomous driving capabilities. 

Awesome! We planned out the ideas necessary to build a driving robot. So we set out to find the necessary parts on Adafruit's website, such as AA batteries, DC Servo motors (which Adafruit stated was ideal for small robots), LiPo battery packs, a Featherwing DC motor driver, and a distance sensor. We ordered these peripherals and set out to slowly figure out how to wire our robot together. There was lots of trial and error occuring when trying to connect the motors, but luckily no electronic was harmed in the process! During this process, we were designing and laser-cutting our robot parts, which were largely inspired by this chassis design:

![Adafruit ESP8266 Mobile Robot](https://cdn-learn.adafruit.com/assets/assets/000/034/447/large1024/microcontrollers_hw5.jpg?1469777542)
https://learn.adafruit.com/build-an-esp8266-mobile-robot

We used Adobe Illustrator to design the parts that were to be laser-cut and used CorelDRAW for any additional tweaks after multiple laser cutting trials. Lots of creative liberty was used in creating the parts, thus the design was finalized on the go. If this had been a more complex robot, use of CAD (computer-aided design) software for modeling the chassis would have been necessary. We did not feel the need to do this for this project as we wanted to put enough energy on the Embedded Systems aspect of the robot, too.

As far as individual parts go, we only designed two of them from scratch on Adobe Illustrator. These parts are the two-inch wheels, motor hangers, and distance sensor cover. The motor hanger is designed to wrap around our blocky DC motor. The distance sensor cover is simply two circles spaced apart. The main chassis, battery pack supports, and axles were cut and glued using other woodshop tools.
  
![Wheel and wheel hanger design](/images/wheel.png)
#### Wheel and wheel hanger design

Since we were already stretching ourselves thin with various extra tasks in the process of making this project come to life, we decided to find existing Micropython libraries that could communicate with the Featherwing directly to drive the motors with ease. We found [this Micropython library](https://github.com/adafruit/micropython-adafruit-pca9685/) that was able to communicate with the Featherwing's onboard PCA9685 chip over 1^2C, a chip with PWM channels that is directly wired to the motor driving chips. We integrated the [pca9685.py](https://github.com/adafruit/micropython-adafruit-pca9685/blob/master/pca9685.py) and [motor.py](https://github.com/adafruit/micropython-adafruit-pca9685/blob/master/motor.py) files and modified them slightly to get them fully compatible with the ESP32's onboard libraries. This was mostly just changing the pca9685's use of the "time" library to "utime"  instead.

Once we got these files compatible and all wires were connected and soldered properly, we created our own [motor controlling drivers](https://github.com/Krizeon/CS435-Robot/blob/master/motorcontrols.py) that calls the functions from motor.py to forward, backward, turn left and turn right functions for our robot. These functions control motors that are connected to the M1 and M2 channels of the Featherwing. From there, the task division fell into place naturally: Kevin wanted to design and build the robot parts, Dylan wanted to implement a wifi-communication system with the ESP32 and design a website with buttons for controlling the device. 

### User Interface 
![Webpage Interface](/images/web_interface.png)

#### Webpage user interface

One of the biggest goals for our project was to have a web interface to control our robot. We figured that this interactive user experience would make our robot much more enjoyable to play with, as opposed to pre-programming some sort of movement routine. Due to Middlebury College’s network restrictions, we were unable to implement the fully functional interface that we had originally envisioned (see the Future Work section), however our version gave us the base functionality that we had envisioned, and was a large part of the success of our robot. 

Inspiration for our WiFi UI was derived from [this example](http://acoptex.com/project/2789/basics-project-076e-esp32-development-board-micropython-web-server-at-acoptexcom/#sthash.7EEX6CQ7.dpbs). Through use of micropython’ socket and network libraries, we were able to configure our ESP32 to function as a web server in our [boot.py file](https://github.com/Krizeon/CS435-Robot/blob/master/boot.py). Upon restarting or booting up, our ESP32 would automatically be set up to function as a web server, with the I.P. address specified in the file and network name and passwords for this server provided in [cred_ap.txt](https://github.com/Krizeon/CS435-Robot/blob/master/cred_ap.txt). 

In our [main.py file](https://github.com/Krizeon/CS435-Robot/blob/master/main.py), the primary program blocks while waiting for connections. Upon receiving a connection, it creates a socket to facilitate communication between the ESP32 and the client and sends raw HTML code (web interface) to the client. At this point, it’s important to give an overview of how our HTML code interfaced with the robot commands. As seen above, our web interface consists of multiple buttons designating different robot direction states. Each button is a hypertext reference to another web page that displays an identical UI (except for the text following “Robot Direction” which is updated to reflect, as one would expect, the robot’s direction). Whenever the client clicks on a button, it communicates to the ESP32 requesting information  for the referenced webpage. The client’s HTTP request includes a header text, specifying which file the client is looking for exactly. The ESP32 parses this header data, and depending on the requested web page, the main program will then set the robot to the associated state, and send the same web page information (except for updated “Robot Direction”) back to the client. Through interacting with buttons on the web page, users are thus able to control the robot through the ESP32’s parsing of HTTP requests. 

### Autonomous Mode
Our implementation of an autonomous mode was overall very simple. The robot would go forward for 25ms. If it then detected an object in front of it within a set threshold (10cm), it would then turn right for 50ms (approximately 90° on the carpet surface we tested on), and repeat. 

Although this was not a complex autonomous mode, incorporating it into the rest of our project made us address some non trivial issues. Since our autonomous was inside an infinite while loop, it was impossible for our robot to remain in autonomous mode while also waiting for client requests from the user to see if they had pressed any buttons. Our solution was to use multithreading, with one thread carrying out web-page related instructions, with the other thread focusing on autonomous mode functionality. With multi-threading being a new concept to both of us, implementing multi-threading into our project was a fun and very rewarding part of the project, allowing us to have a core part of the original functionality that we had originally envisioned. 

![sonar picture](/images/sonar_picture.jpeg)

#### Initial testing of distance sensor

### Bill of Materials

  * Adafruit Huzzah32: $19.95
  * US-100 Ultrasonic Distance Sensor: $6.95
  * DC Motor + Stepper FeatherWing: $21.50
  * DC Motor: $3.50 x 2 = $7.00
  * Lithium Ion Polymer Battery 3.7v 1200m: $9.95
  * 4 x AA Battery Holder: $2.95
#### Total Project Cost: $68.30



## Results

[![VIDEO](http://img.youtube.com/vi/MpUsSLf8D8k/0.jpg)](http://www.youtube.com/watch?v=MpUsSLf8D8k)

#### Demonstration Video

As seen in this short video, our robot works! The first half of the video demonstrates the robot’s autonomous mode as Dylan manually places his foot in front of the robot to force it to demonstrate its ability to avoid obstacles. Towards the end of the video, the robot is switched from autonomous mode to manual mode in which the user causes to robot to go forward, stop, then go backwards. 

Although it would have been ideal for the video to have included a more thorough demonstration of all of the robot’s directions, as well as showing the interaction between the web page interface with the robot, this video allows us to see the multiple parts of our project properly communicate and work together. 



## Schedule

Our original schedule was as follows:

  * Week 1: Order, receive, and put together robot parts/materials
  * Week 2: Ensure proper communication between board and peripherals, create basic autonomous mode
  * Week 3-4: Dylan: Create WiFi communication interface; Kevin: Flesh out autonomous mode and create high quality chassis for robot 
  * Week 5: Create final project webpage, general code debugging

Our actual schedule ended up changing quite a bit due to parts not being delivered on time, among other issues. It resulted in the following:

  * Week 1: Come up with project, figure out necessary parts
Dylan: Distance Sensor
Kevin: Solder FeatherStepper to HUZZAH ESP32, DC motors
  * Week 2-3: Dylan: User Interface (Website), Autonomous Mode; Kevin: Build robot chassis, wheels using laser cutter
Order more materials (Batteries!)
  * Week 4: Address remaining bugs, construct remaining robot parts needed (sensor holder)
  * Week 5: Work on presentation, webpage

Despite some hiccups, we had a good working schedule. We were able to complete the bulk of the robot and code in a timely manner. 



## Issues Encountered
Although we encountered a variety of issues during the building and coding of this robot, we were able to resolve most all of them to ultimately create a fully functional product. 

### Libraries
Many of the available libraries we found (for our peripherals such as DC Motors, Stepper Featherwing) were for CircuitPython, which required us to find third party libraries 

Building the chassis and robot also took more time than anticipated. We went through several trial and errors to refine our designs for the laser cutter. We tried using chipboard, lumber, plywood, but eventually settled on hardboard for the wheels and thin plywood for the motor hangers. The construction of the support for the battery pack was done on the spot, and that took some experimenting with glue, toothpicks, and sheets of wood.

### Missing Components
At the start of our project, we started out with only our Huzzah32, distance sensor, stepper featherwing, and DC motors. Although we were able to get these parts communicating well within the first few weeks, we were restrained by the robot always needing to be connected to our computers as a power source. We quickly came to realize that without batteries, it would be hard to progress and fully test whether our physical components and actually code worked effectively when the robot was free roaming. And then once we did finally receive all the materials, the trick was figuring out how to place fit them onto the robot...

![build image](/images/build_test.jpeg)

#### Initial built testing of distance sensor, battery, and battery pack placement on robot

### Multithreading
It was both of our first times working with multiple threads, and we encountered several problems along the way due to our original single-thread minded code not being structured to handle multiple threads. However, After playing around with the _thread library and getting some experience under our belts, we were able to resolve these issues. 



## Future Work
Overall, we're very happy with how our project turned out! It was a fantastic experience having to go through the research, trial, and troubleshooting phases of building an embedded system project. However, some aspects of our project that we'd like to improve are the autonomous mode, turning, user interface, and robot construction. 

### Autonomous Mode
Our current implementation of autonomous mode is pretty simplistic - it boils down to "go forward, and turn right if an obstacle appears in front of the robot." This was adequate for our project, as the focus of this build wasn’t the autonomous mode, but rather the wholstic creation and implementation of an embedded system. As it was, our autonomous mode worked to ensure that our various peripherals (motors, distance sensor) were working correctly, and was fun to watch as it maneuvered throughout our classroom. However, creating a more thorough and robust autonomous would be the logical upgrade to our project. Having our robot able to make its way from point A to point B using various searching algorithms would be a fun project, especially now that we have a physical robot we can use to test with. This would likely require adding more sensors to our robot, as our current implementation with a single sensor will not register objects except those directly in front of it, causing it to occasionally run into objects it’s not perpendicular to. Utilizing 2 or 3 distance sensors would give us more information to work with when developing an autonomous mode program, and ultimately enhance the type of algorithms we could use. 

In a similar vein of thought, another aspect of the autonomous mode that we’d like to improve is how the distance sensor readouts are used. Currently, the autonomous reads the distance from the distance sensor every 50ms. While this is adequate for the current speeds our robot moves at and the distance thresholds we’ve set, a more elegant solution would be to connect the sensor to an ISR or run it in a new thread. In a multithreading scenario, we would have the get_distance thread send a signal to the main thread, which would handle the signal by stopping the robot, maneuvering the robot to a position in which it would no longer crash, then hand the reins back to the default autonomous mode. This implementation could also be made useful in regular user-control modes, where the would automatically stop the robot if it ever thought it was about to crash, regardless of the user’s input. 

### Turning
Our current implementation for turning is done by turning the rear wheels connected to the DC motors in opposite directions. For example, to turn left, the rear left wheel reverses, while the front right wheel goes forward. This results in the robot turning on the spot, but is overall not a fluid motion, especially since the front wheels are partially dragged in order to complete the tight turn. One improvement could be to create a turning method with a larger turning radius, similar to how a car would turn. This could be done by turning both powered wheels forward, but at different speeds. Another option could be using [mecanum wheels](https://www.andymark.com/products/4-in-hd-mecanum-wheel-set-options) which are able to turn and move sideways seamlessly, even without steering systems. 

### User Interface
The round-about method in which we created a WiFi control interface for our robot was due to the various network restrictions Middlebury College. As a result, there was a significant amount of control features that we would have liked to implement, but were unable to due to the limitations of the system we had to resort to using. With a more open network, we would have been able to implement a more interactive interface that allowed for more functionality beyond direction buttons and autonomous mode. Some simple improvements would be the addition of sliders next to the directional buttons to designate speed. Our motor driver functions take motor-speed as a parameter, however due to our web interface not being able to translate slider values back to the robot, we had to hardcode a motor speed into our functions despite the variable speed potential. 

If we were to completely rework our UI, something that we would like to focus is a mobile interface. Some big advantages of the touch screen functionality that provides would be virtual joystick controls, or even taking advantage of smart phone’s internal gyroscopes to provide controls by tilting the phone in various directions. 

### Robot Construction
In the time frame provided, we were able to make what is (in our opinion) a very sleek and well put together robot chassis. Kevin’s diligence on the laser cutter and soldering experience allowed us to have a very compact, yet functional final product. However, with more time on our hands, we would have likely decided to make more robust wheels with greater traction, a thicker distance sensor holder, and an encapsulating housing for our ESP32 and battery packs. 



## References
  * https://www.geeksforgeeks.org/python-bytearray-function/
  * https://forum.micropython.org/viewtopic.php?t=762
  * https://docs.espressif.com/projects/esp-idf/en/latest/esp32s2beta.html
  * https://docs.micropython.org/en/latest/library/_thread.html
  * https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/thread
  * https://learn.adafruit.com/adafruit-stepper-dc-motor-featherwing/circuitpython
  * http://acoptex.com/project/2789/basics-project-076e-esp32-development-board-micropython-web-server-at-acoptexcom/#sthash.jI4TOzgE.dpbs
  * https://github.com/Krizeon/CS435-Robot/blob/master/README.md
  * https://www.sltrib.com/news/2019/08/19/yelling-siri-or-alexa/


![robot_face](/images/robot_front.jpeg)

