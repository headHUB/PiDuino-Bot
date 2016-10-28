# Code for operating a small home-built robot over wifi, using Python 2.

please take note that, for the face detection to work, this project should have a /haarcascades folder in it, [this one](https://github.com/opencv/opencv/tree/master/data/haarcascades) to be exact.

Includes uv4l camera stream display, remote control using tcp packets, sonar feedback, and a little bit of face recognition (still working on a neural net implementation).

run connect_serial3.ino on the arduino, and connect it via usb serial. this handles collecting sonar data, communication with the raspberry, and the running the engines.

run arduino_command_center3.py on the raspberry pi. default IP is set to 192.168.0.105. this will start managing the serial and tcp connections, and provide all the decoding and encoding of commands and feeback.

run both tryout_command_gui.py and display_video_stream2.py on your command console (pc/laptop). 
the first one starts a small window which you can use to control the robot's movement by pressing and holding q,w,e,a,s, or d to drive.
the second one opens the uv4l mjpg video stream from the raspberry pi's camera. it also performs some basic face detection (viola-jones) using cv2.

the next step is some robust face detection, then personal classification (telling different people or pets apart), and finally personalized responses.

this project uses a raspberry pi b+, an arduino uno, with a sensor shield v5, sonar module, and a motor control board, a raspi camera, cheap usb wifi dongle, all mounted on a robot base with 4 wheels. a tie-wrap may have been used. or not. i'm not telling, don't judge me.
