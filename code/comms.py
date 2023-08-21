#!/usr/bin/env python3

import bluetooth

class State:
	OFFLINE = 0
	FINDING = 1
	ATTACKING = 2
	DEFENDING = 3

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

state = State.OFFLINE

def Server():
	server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

	server.bind(("",bluetooth.PORT_ANY))
	server.listen(1)

	ip,port = server.getsockname()


	bluetooth.advertise_service(
		server, 
		"RobotServer", 
		service_id=uuid,
		service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
		profiles=[bluetooth.SERIAL_PORT_PROFILE],
	)

	print(ip,port)

	client, info = server.accept()

	print(client,info)

	client.close()
	server.close()

def Client():
	service_matches = bluetooth.find_service(uuid=uuid)

	server = service_matches[0]

	print(server)

	client = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	client.connect((server["host"], server["port"]))

	client.close()

def Start():
	pass