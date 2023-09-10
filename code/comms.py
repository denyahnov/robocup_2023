#!/usr/bin/env python3

import socket
from time import sleep
from json import loads,dumps
from threading import Thread
from traceback import print_exc

global state, my_data, other_data

class sensors:
	ball_strength = 0

class State:
	OFFLINE = 0
	PAUSED 	= 1
	CONNECTED = 2

global host, port

host, port = "2C:6D:C1:08:83:B9", 4
# host, port = "00:17:E9:B1:9F:04", 4

state = State.OFFLINE
my_data, other_data = {}, {}

def UpdateData(values):
	global state,my_data

	my_data = {
		"state": state,
		"ball_strength": values.ball_strength,
	}

def Send(robot_socket):
	global my_data

	robot_socket.send(dumps(my_data).encode('utf-8'))

def Receive(robot_socket):
	global other_data

	data = robot_socket.recv(1024)

	other_data = loads(data.decode('utf-8'))

def Server():
	global state
	global host, port

	server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
	server.bind((host,port))

	server.listen()

	print("Waiting for client at {}, {}".format(host,port))

	client,addr = server.accept()

	print("Client connected at {}".format(addr))

	state = State.CONNECTED

	return client,server

def Client():
	global state
	global host, port

	client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
	client.settimeout(3)

	client.connect((host, port))

	state = State.CONNECTED

	return client,client

def CreateSocket():
	try:
		return Client(), True
	except:
		return Server(), False

def connected_thread(robot_socket, main_socket, is_client):
	global state

	try:
		while state != State.OFFLINE:
			UpdateData(sensors)

			if is_client:
				Send(robot_socket)
				sleep(0.1)
				Receive(robot_socket)
				sleep(0.1)
			else:
				Receive(robot_socket)
				sleep(0.1)
				Send(robot_socket)
				sleep(0.1)

			print(other_data)
	except:
		print_exc()

	state = State.OFFLINE

	main_socket.close()

def main_loop(brick,sensors):
	global state

	if brick != None:
		brick.Color('orange')

	try:
		(robot_socket, main_socket), is_client = CreateSocket()
	except:
		print_exc()

		if brick != None:
			brick.PlayTone(300,0.2)
		
			brick.Color('green')

		return

	if brick != None:
		brick.PlayTone(650,0.2)

		brick.Color('green')

	print("Robots Linked!")

	thread = Thread(target=connected_thread,args=[robot_socket, main_socket, is_client])
	thread.daemon = True

	thread.start()

if __name__ == '__main__':
	brick = None

	# import brick

	main_loop(brick,sensors)

	import random

	while True:
		sensors.ball_strength = random.randint(30,140)
		sleep(0.5)