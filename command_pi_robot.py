# quick robot control over UTP via command line
# gebruik samen met udp_server.py op de pi (wordt: arduino_command_center2.py)

import socket
import termios, fcntl, sys, os, time


# input setup
fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

# command line options
# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

# last time a key was pressed
last_keypress = time.time()

# utp setup
TCP_IP = '192.168.0.105'
TCP_PORT = 5005
BUFFER_SIZE = 1024
# MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


try:
    while 1:
        try:
			if(time.time() - last_keypress > 0.55):
				print "stop"
				s.send(".")
				last_keypress += 10000
			c = sys.stdin.read(1)
			last_keypress = time.time()
			print "Got character", repr(c)

			s.send(c)
			# data = s.recv(BUFFER_SIZE)
			# print "received back", data
			# s.close()
        except IOError: pass
# except if(time.time() - last_keypress > 0.3):
# 	print "stop"
# 	last_keypress += 10000
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



# while 1:
# 	try:
# 		if(time.time() - last_keypress > 0.55):
# 			print "stop"
# 			s.send(".")
# 			last_keypress += 10000
# 			# data = s.recv(BUFFER_SIZE)
# 			# print "received back", data
# 		else:
# 			try:
# 				c = sys.stdin.read(1)
# 				last_keypress = time.time()
# 				print "Got character", repr(c)
# 				s.send(c)
# 				data = s.recv(BUFFER_SIZE)
# 				print "received back", data
# 			except KeyboardInterrupt:
# 				print "OK NU KAPPEN"
# 				termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
# 				fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
# 				sys.exit()
# 	except IOError: pass
# 	finally:
# 	    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
# 	    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)


# except if(time.time() - last_keypress > 0.3):
# 	print "stop"
# 	last_keypress += 10000
# except (KeyboardInterrupt, SystemExit):
#     raise
#     termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
#     fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
# except:
# 	print "ohnee"





# OUD MAAR WERKEND
# try:
#     while 1:
#         try:
# 			if(time.time() - last_keypress > 0.45):
# 				print "stop"
# 				s.send("stop")
# 				last_keypress += 10000
# 			c = sys.stdin.read(1)
# 			last_keypress = time.time()
# 			print "Got character", repr(c)

# 			s.send(c)
# 			data = s.recv(BUFFER_SIZE)
# 			print "received back", data
# 			# s.close()
#         except IOError: pass
# # except if(time.time() - last_keypress > 0.3):
# # 	print "stop"
# # 	last_keypress += 10000
# finally:
#     termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
#     fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)