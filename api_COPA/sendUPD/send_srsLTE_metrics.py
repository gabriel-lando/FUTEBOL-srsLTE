import time
import re
import time
import sys

import json
import socket

UDP_IP = "UDP_SERVER_IP_ADDRESS"
UDP_PORT = 5005

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_dest = (UDP_IP, UDP_PORT)



file = open("enodeb.txt", "r+")
while True:
	line = file.read()
	result = str(line).replace(" ", ",")
	result1 = result.replace(",,,", ",")
	result2 = result1.replace(",,,", ",")
	result3 = result2.replace(",,", ",")

	#rnti     cqi      ri          mcs           brate                     bler             snr             phr               mcs                                brate                       bler
	m = re.compile('(.*?(\d{2}|\d{1,}\w{1}),\d{1,}.\d{1,},\d{1},\d{1,}.\d{1,}),(\d{1,}.\d{1,}\w{1}|\d{1,}.\d{1,}),(\d{1,}.\d{1,}%|\d{1,}%),(\d{1,}.\d{1,}),(\d{1,}.\d{1,}),(\d{1,}.\d{1,}),(\d{1,}.\d{1,}\w{1}|\d{1,}.\d{1,}),(\d{1,}.\d{1,}%|\d{1,}%),(\d{1,}.\d{1,})')
	res = m.findall(result3)

	for i in res:
		# parse
		string = ','.join(i)
		removeK = string.replace("k","") #remove k
		result = removeK.replace("%","") #remove %
		vector = result.split(",")
		mega = 0

		if str(vector[6]).find("M") != -1:
			#1000
			splipMega = str(vector[6]).replace("M","") #remov M
			mega = float(splipMega)*1024
		else:
			mega = float(vector[6])

		if float(vector[8]) != 0:
			data = {}
			data['id'] = vector[1]
			data['brate'] = mega
			data['snr'] = float(vector[8])
			json_data = json.dumps(data)
			print json_data
			udp.sendto(json_data, udp_dest)

