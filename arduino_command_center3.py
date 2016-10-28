# gebaseerd op https://github.com/pnetherwood/ArmControlPiPython/blob/master/arm_server.py

import socket
import sys
import struct
import time
import serial
from thread import *



# command receive socket setup
HOST = '' # Symbolic name meaning all available interfaces
PORT_RECEIVE = 5005 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow socket reuse
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((HOST,PORT_RECEIVE))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.listen(10)

# distance send socket setup
PORT_SEND = 5006 # Arbitrary non-privileged port

s_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow socket reuse
s_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s_send.bind((HOST,PORT_SEND))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s_send.listen(10)

# thread for receiving commands from master
def clientthread(conn):
    # Keep running until quit command executed
    while 1:
        # Get the data
        data = conn.recv(1)

        if not data:
            print "Socket closed"
            break

        # Strip off any whitespace if present
        data = ''.join(data.split())

        # Loop through the recieved buffer a character at a time building up commands
        i = 0;
        cmd = ""
        while i < len(data):
            # Look for the special case of arm stop
            if data[i] == '.':
                # stop()
                # print "stop"
                ser.write(b'4\n')
                i += 1
                time.sleep(.1)
                cmd = ""
                continue

            # Build up command
            cmd += data[i]

            if len(cmd) == 1:
                if cmd == ".":
                    print "sending stop"
                    ser.write(struct.pack('!B',1))
                elif cmd == "q":
                    ser.write(struct.pack('!B',2))
                elif cmd == "w":
                    ser.write(struct.pack('!B',3))
                elif cmd == "e":
                    ser.write(struct.pack('!B',4))
                elif cmd == "a":
                    ser.write(struct.pack('!B',5))
                elif cmd == "s":
                    ser.write(struct.pack('!B',6))
                elif cmd == "d":
                    ser.write(struct.pack('!B',7))
                elif cmd in "zxc":
                    ser.write(b'zxc')
                elif cmd == "t":
                    ser.write("102\n")
                # Clear command once issued
                cmd = ""
            data = ""


def serverthread(conn):
    while 1:
        distance = ser.readline()  # leest een line met \n op einde, read gebruiken en opbouwen met ints/bytes?
        # print type(distance)
        if distance == '101\n':
            print "dat was een q!"
            # print len(distance)
            # print distance
        elif distance == '267\n':
            print "dat was een w!"
        elif distance == '100\n':
            print "kutje"
            print len(distance)
        elif distance == '7':
            print "gewoon 7"
        elif distance == '7\n':
            print "7 met newline"
        elif distance == '1\n':
            print "dat was toch echt q"
        elif '102' in distance:
            print "102 get"
            print repr(distance)
        else:
            print "distance is", repr(distance)
            # print len(distance)
            conn.send(distance)
        time.sleep(.1)

##
## Main starting point of server
## 
running = True
try:
    while running:
        print "Waiting ..."
        # Wait to accept a connection from master
        conn, addr = s.accept()
        print 'Connected command link with ' + addr[0] + ':' + str(addr[1])

        conn_send, addr_send = s_send.accept()
        print 'Connected sensor link with ' + addr_send[0] + ':' + str(addr_send[1])

        # serial setup
        # open and reset serial
        ser = serial.Serial('/dev/ttyACM0',9600)
        ser.close()
        ser.open()
        time.sleep(.5)

        # Start listening to new socket on seperate thread
        start_new_thread(clientthread ,(conn,))
        start_new_thread(serverthread ,(conn_send,))
  
finally:
    print "Exiting"
    try:
        arm.stop()  # Stop the arm if we get here in error
    except:
        pass
    s.close()
    time.sleep(0.1) # wait a little for threads to finish
