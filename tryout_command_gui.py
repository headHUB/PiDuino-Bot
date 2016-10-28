# robot control GUI tryout

import socket
import time
import os
from Tkinter import *

# gui setup
root = Tk()

# keypress setup
sent_flag = False
last_time = time.time()
time_between_keys = 0.01
os.system('xset r off')

# utp setup
TCP_IP = '192.168.0.105'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))



def key(event):
	global last_time
	if(time.time() - last_time > time_between_keys):
		last_time = time.time()
		print "pressed", repr(event.char)
		s.send(event.char)
	else:
		last_time = time.time()

def keyrelease(event):
	global last_time
	if(time.time() - last_time > time_between_keys):
		last_time = time.time()
		print "released", repr(event.char)
		s.send(".")
	else:
		last_time = time.time()

def callback(event):
	frame.focus_set()
	print "clicked at", event.x, event.y

frame = Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.bind("<KeyRelease>", keyrelease)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()
os.system('xset r on')