# main.py

# ESP32 will host a webpage accessible by connecting to its WiFi and maneuvering
# to the IP address specified in boot.py. Webpage is used to control robot. 

import usocket as us
from motorcontrols import *
import _thread

# initial robot state is stopped/braking
robot_direction = 100
brake()

# Configure the socket
s = us.socket(us.AF_INET, us.SOCK_STREAM)

# Listen to incoming connections on port 80 and respons at most at 1 conenction at a time
s.bind(('', 80))
s.listen(1)


def web_page():
    """
    returns a webpage with button controls for robot
    """
    
    # robot_direction variable used for updating HTML code to display robot's current status
    global robot_direction

    # update robot's status on webpage
    if robot_direction == 0:
        direction_string = "FORWARD"
    elif robot_direction == 1:
        direction_string = "BACKWARDS"
    elif robot_direction == 2:
        direction_string = "LEFT"
    elif robot_direction == 3:
        direction_string = "RIGHT"
    elif robot_direction == 100:
        direction_string = "STOPPED"
    elif robot_direction == 4:
        direction_string = "AUTONOMOUS"

    # webpage code
    html = """<html>
             <head>
              <title>ESP32 Web Server</title>
              <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="icon" href="data:,">
              <style>
               html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
               h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
               .button{display: inline-block; background-color: #FF6A00; border: none; border-radius: 4px;
                       color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
               .button2{display: inline-block; background-color: #4CFF00; border: none; border-radius: 4px;
                        color: white; padding: 16px 30px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
              </style>
            </head>
            <body>
             <h1>ROBOT CONTROLS</h1>
             <p>Robot direction: <strong>""" + direction_string + """</strong></p>
             <p><a href="/forward"><button class="button2">FORWARD</button></a></p>
             <p><a href="/left"><button class="button2">LEFT</button></a>
             <a href="/right"><button class="button2">RIGHT</button></a></p>
             <p><a href="/backwards"><button class="button2">BACKWARDS</button></a></p>
             <p><a href="/stopped"><button class="button2">STOPPED</button></a></p>
             <p><a href="/autonomous"><button class="button2">AUTONOMOUS</button></a></p>
             <p></p>
             <p></p>
            </body>
           </html>"""

    return html

# loop forever
while True:
    # Accept incoming connections
    cl, addr = s.accept()
    print('Got a connection from %s' % str(addr))

    # Handle the socket as if it was a binary file, allows us to use readline()
    cl_file = cl.makefile('rwb', 0)
    
    # read through HTTP header file
    while True:
        line = cl.readline()

        # If no line or empty line, we are done
        # A GET request will end with an empty line after the header
        # A POST request will have an empty line between the header and the body
        if not line or line == b'\r\n':
            break

        # if line starts with Get, button was pressed and need to update robot state
        if line.startswith(b'GET '):
            print(line)
            # split header line to isolate page user moved to - that's the robot state to change to
            url = line.split(b' ')[1].split(b'/')

            # do stuff depending on what button was pressed
            if url[1] == b'forward':
                print("FORWARD")
                robot_direction = 0
                forward(50)
            elif url[1] == b'backwards':
                print("BACKWARDS")
                robot_direction = 1
                backward(50)
            elif url[1] == b'left':
                print("LEFT")
                robot_direction = 2
                left(50)
            elif url[1] == b'right':
                print("RIGHT")
                robot_direction = 3
                right(50)
            elif url[1] == b'stopped':
                print("STOPPED")
                robot_direction = 100
                brake()
            elif url[1] == b'autonomous':
                print("AUTONOMOUS")
                robot_direction = 4
                # in order to poll webpage for other buttons pressed, while havinging the 
                # autonomous mode inside an infinite loop, have to multi thread
                _thread.start_new_thread(autonomous_drive, ())

    # Send back the dynamic webpage response
    response = web_page()
    cl.send(response)

    # Close the connection
    cl.close()
