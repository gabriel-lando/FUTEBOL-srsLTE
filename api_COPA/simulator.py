import requests
from threading import Thread
import random
from pprint import pprint
import time

import re
import sys
import json, os

class COPASimulator(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.exec_flag = True
        self.addr = "10.0.2.8"
        self.protocol = "http"
        self.port = 8000
        self.rooturl = "%s://%s:%d" % (self.protocol, self.addr, self.port)
        self.rootnetwork = "%s/REST/network" % (self.rooturl)
        self.interval = 1
        self.pool = self.getPool()
        self.path = "/"

        print("Pool chosen: "+self.pool)

    # def generateData(self):
    #     raise NotImplementedError()
        
    def setPool(self, pool):
        self.pool = pool

        return True
    
    def setPath(self, path):
        if not path.endswith("/"):
            path = path + "/"
        
        self.path = path

        return True

    def getPool(self):
        url = "%s/REST/pools" % self.rooturl
        
        response = requests.get(url)
        data = response.json()
        pprint(data)

        if data:
            if data["pools"]:
                pools = data["pools"]
                if pools[1]:
                    return pools[1][0]

        return None

    def sendData(self, data):
        url = self.rootnetwork+self.path

        try:
            response = requests.post(url, data)

            if response.status_code == 200:
                pprint(data)
                pprint(response.json())
            else:
                print("Error: ", response.status_code)
                print("Error: ", response.text)
        except:
            print("Agent was not able to send data to server")
        
        return True

    def run(self):

        file = open("enodeb.txt", "r+")
        file.truncate(0)

        while self.exec_flag:
            try:
                line = file.readline()

                if line is None:
                    break

                else:
                    result = str(line).replace(" ", ",")
                    result1 = result.replace(",,,", ",")
                    result2 = result1.replace(",,,", ",")
                    result3 = result2.replace(",,", ",")

                    #                   rnti                           cqi             ri  mcs             brate                               bler                    snr             phr             mcs             brate                               bler                    bsr             tx              rx
                    m = re.compile('(.*?(\d{2}|\d{1,}\w{1}|\w{1}\d{1,}),\d{1,}.\d{1,},\d{1},\d{1,}.\d{1,}),(\d{1,}.\d{1,}\w{1}|\d{1,}.\d{1,}),(\d{1,}.\d{1,}%|\d{1,}%),(\d{1,}.\d{1,}),(\d{1,}.\d{1,}),(\d{1,}.\d{1,}),(\d{1,}.\d{1,}\w{1}|\d{1,}.\d{1,}),(\d{1,}.\d{1,}%|\d{1,}%),(\d{1,}.\d{1,}),(\d{1,}.\d{1,}),(\d{1,}.\d{1,})')
                    res = m.findall(result3)

                    for i in res:
                        # parse
                        string = ','.join(i)
                        removeK = string.replace("k","") #remove k
                        result = removeK.replace("%","") #remove %
                        vector = result.split(",")
                        mega_dl = 0
                        mega_ul = 0

                        if str(vector[5]).find("M") != -1:
                            #1000
                            splipMega = str(vector[5]).replace("M","") #remov M
                            mega_dl = float(splipMega)*1000
                        else:
                            mega_dl = float(vector[5])

                        if str(vector[10]).find("M") != -1:
                            #1000
                            splipMega = str(vector[10]).replace("M","") #remov M
                            mega_ul = float(splipMega)*1000
                        else:
                            mega_ul = float(vector[10])

                        if float(vector[7]) != 0:
                            data = {}
                            data['locus'] = self.pool
                            data['rnti'] = vector[0]
                            data['dl_cqi'] = float(vector[1])
                            data['dl_ri'] = float(vector[2])
                            data['dl_mcs'] = float(vector[3])
                            data['dl_brate'] = mega_dl
                            data['dl_bler'] = float(vector[6])
                            data['ul_snr'] = float(vector[7])
                            data['ul_phr'] = float(vector[8])
                            data['ul_mcs'] = float(vector[9])
                            data['ul_brate'] = mega_ul
                            data['ul_bler'] = float(vector[11])
                            data['ul_bsr'] = float(vector[12])
                            data['tx_gain'] = float(vector[13])
                            data['rx_gain'] = float(vector[14])
                            self.sendData(data)

                time.sleep(self.interval/100)

                # data = self.generateData()

                # self.sendData(data)

                # time.sleep(self.interval)
            except:
                print("Something gone wrong at COPASimulator.")
                self.exec_flag = False
                raise

    def stop_thread(self):
        self.exec_flag = False