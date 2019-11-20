# webpage_controller.py

import usocket as us

robot_direction = 100

# Configure the socket
s = us.socket(us.AF_INET, us.SOCK_STREAM)
# Listen to incoming connections on port 80 and respons at most at 1 conenction at a time
s.bind(('', 80))
s.listen(1)


def web_page():
    """
    Will return a web page with dynamic information about the LED status
    """

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

    # This is the page content
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
             <div class="slidecontainer">
                <input type="range" min="1" max="100" value="50" class="slider" id="myRange">
             </div>
             <p>Robot direction: <strong>""" + direction_string + """</strong></p>
             <p><a href="/forward"><button class="button2">FORWARD</button></a></p>
             <p><a href="/left"><button class="button2">LEFT</button></a>
             <a href="/right"><button class="button2">RIGHT</button></a></p>
             <p><a href="/backwards"><button class="button2">BACKWARDS</button></a></p>
             <p><a href="/stopped"><button class="button2">STOPPED</button></a></p>
             <p></p>
             <p></p>
            </body>
           </html>"""

    return html

# Loop forever
while True:
    # Accept incoming connections
    cl, addr = s.accept()
    print('Got a connection from %s' % str(addr))

    # Handle the socket as if it was a binary file, allows us to use readline()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl.readline()

        # If no line or empty line, we are done
        # A GET request will end with an empty line after the header
        # A POST request will have an empty line between the header and the body
        if not line or line == b'\r\n':
            break

        # Let's look for GET methods: they want some data from our server
        if line.startswith(b'GET '):
            # Brake it apart using spaces (separated GET from the following URL)
            # and then break the URL in part based on '/'
            # How the URL looks like will depend on your API
            url = line.split(b' ')[1].split(b'/')

            # do stuff depending on what button was pressed
            if url[1] == b'forward':
                print("FORWARD")
                robot_direction = 0
            elif url[1] == b'backwards':
                print("BACKWARDS")
                robot_direction = 1
            elif url[1] == b'left':
                print("LEFT")
                robot_direction = 2
            elif url[1] == b'right':
                print("RIGHT")
                robot_direction = 3
            elif url[1] == b'stopped':
                print("STOPPED")
                robot_direction = 100

    # Send back the dynamic response
    response = web_page()
    cl.send(response)

    # Close the connection
    cl.close()
