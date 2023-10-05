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

global host_client, host_server, port

# Go to 'Network & Connections' tab 
# Set Bluetooth to 'Powered', 'Visible' and 'Start Scan'
# Find the other robot in the 'Scanned Devices' page and connect to it
# Confirm whatever popup appears
# Get the bluetooth address and put it into here

# 'hciconfig' on Linux
# 'ipconfig /all' on Windows

addresses = {
	"Dennis Laptop": "2C:6D:C1:08:83:B9",
	"Dennis Home Robot": "00:17:E9:B1:9F:04",
	"Green Robot": "24:71:89:49:AE:45",
	"Multicolor Robot": "CC:78:AB:34:70:7C",
}

# GREEN ROBOT 	= ID 0
# MULTICOLOR 	= ID 1

def InitComms(calibration):
	global host_client, host_server, port

	host_server = addresses[["Green Robot", "Multicolor Robot"][calibration.robot_id]]
	host_client = addresses[["Green Robot", "Multicolor Robot"][calibration.robot_id - 1]]

	port = 4

state = State.OFFLINE
my_data, other_data = {}, {}

def UpdateData(sensors):
	global my_data

	my_data = {
		"state": sensors.Values.robot_running,
		"ball_strength": sensors.Values.ball_strength,
		"has_ball": sensors.Values.has_ball,
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
	global host_server, port

	server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
	server.bind((host_server,port))

	server.listen()

	print("Waiting for client at {}".format(host_server))

	client,addr = server.accept()

	print("Client connected at {}".format(addr[0]))

	state = State.CONNECTED

	return client,server

def Client():
	global state
	global host_client, port

	client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
	client.settimeout(10)

	client.connect((host_client, port))

	state = State.CONNECTED

	return client,client

def CreateSocket():
	try:
		return Client(), True
	except socket.timeout:
		return None
	except:
		return Server(), False

def connected_thread(brick, sensors, robot_socket, main_socket, is_client):
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

	brick.PlayTone(410,0.1)
	brick.PlayTone(390,0.1)
	brick.PlayTone(380,0.1)

def Connect(brick,sensors):
	global state

	if state == State.CONNECTED:
		brick.PlayTone(300,0.1)
		return

	brick.Color('orange')

	try:
		(robot_socket, main_socket), is_client = CreateSocket()

		print(["Server","Client"][int(is_client)])
	except:
		print_exc()

		brick.PlayTone(300,0.2)
		
		brick.Color('green')

		return

	brick.PlayTone(650,0.2)

	brick.Color('green')

	print("Robots Linked!")

	thread = Thread(target=connected_thread,args=[brick, sensors, robot_socket, main_socket, is_client])
	thread.daemon = True

	thread.start()