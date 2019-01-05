import socket
import select
import sys
import time
import getopt

PRIMARYIP = "192.168.1.7"
PRIMARYPORT = 19761

BACKUPIP = "192.168.1.10"
BACKUPPORT = 19764

EMERGIP = "192.168.1.10"
EMERGPORT = 19764

try:
	opts, args = getopt.getopt(sys.argv[1:],"p:l:")
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

while(True):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((PRIMARYIP,PRIMARYPORT))
		print("Connected to Primary");
	except socket.error:
		try:
			sock.connect((BACKUPIP,BACKUPPORT))
			print("Connected to Backup");
		except socket.error:
			try:
				sock.connect((EMERGIP,EMERGPORT))
				print("Connected to Emergency");
			except socket.error:
				print("None of the specified servers are currently available");
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
	except socket.error:
		print("Connection Lost");
		time.sleep(1)
