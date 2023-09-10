#!/usr/bin/env python3

import socket
from time import sleep
from json import loads,dumps
from threading import Thread
from traceback import print_exc

global state, my_data, other_data

class State:
	OFFLINE = 0
	CONNECTED = 1

	RUNNING = False

global host, port

host, port = "2C:6D:C1:08:83:B9", 4
# host, port = "00:17:E9:B1:9F:04", 4

state = State.OFFLINE
my_data, other_data = {}, {}

def UpdateData(sensors):
	global my_data

	my_data = {
		"state": State.RUNNING,
		"ball_strength": sensors.Values.ball_strength,
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

	print("Waiting for client at {}".format(host))

	client,addr = server.accept()

	print("Client connected at {}".format(addr[0]))

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

def connected_thread(brick, robot_socket, main_socket, is_client):
	global state

	TPS = 20

	try:
		while state != State.OFFLINE:
			UpdateData(sensors)

			if is_client:
				Send(robot_socket)
				sleep(0.5 / TPS)
				Receive(robot_socket)
				sleep(0.5 / TPS)

			else:
				Receive(robot_socket)
				sleep(0.5 / TPS)
				Send(robot_socket)
				sleep(0.5 / TPS)

	except:
		print_exc()

	state = State.OFFLINE

	main_socket.close()

	if brick != None:
		brick.PlayTone(410,0.1)
		brick.PlayTone(390,0.1)
		brick.PlayTone(380,0.1)

def Connect(brick,sensors):
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

	thread = Thread(target=connected_thread,args=[brick, robot_socket, main_socket, is_client])
	thread.daemon = True

	thread.start()