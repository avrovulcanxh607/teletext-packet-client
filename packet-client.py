import socket
import select
import sys
import time
import getopt
import os

PRIMARYIP = "192.168.1.10"
PRIMARYPORT = 19761

BACKUPIP = "192.168.1.7"
BACKUPPORT = 19761

try:
	opts, args = getopt.getopt(sys.argv[1:],"p:l:")
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

while(True):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((PRIMARYIP,PRIMARYPORT))
		with open("/home/pi/databridge.log", "w") as f:
			f.write("Primary")
	except socket.error:
		try:
			sock.connect((BACKUPIP,BACKUPPORT))
			with open("/home/pi/databridge.log", "w") as f:
				f.write("Backup")
		except socket.error:
			with open("/home/pi/databridge.log", "w") as f:
                                f.write("Not Connected")
			os.system('cat' ' /home/pi/offairdata.raw')
			sys.exit(2)

	try:
		sock.sendall(bytes("HELO", "utf-8"))
		starttime = time.time()
		while(True):
			inputready, outputready, exceptready = select.select([sock], [], [], 0 )
			if inputready:
				received = sock.recv(672)
				sys.stdout.buffer.write(received)
			time.sleep(0.02 - ((time.time() - starttime) % 0.02))

	except:
		with open("/home/pi/databridge.log", "w") as f:
			f.write("Connection Lost")
