import requests
from threading import Thread
import random
from pprint import pprint
import time


from simulator import COPASimulator
class LTESimulator(COPASimulator):
    def __init__(self):
        COPASimulator.__init__(self)

    # def generateData(self):
    #     return {
    #     "locus": self.pool,
    #     "dl_ri": round(random.random(), 2), 
    #     "dl_bler": round(random.random(), 2), 
    #     "dl_mcs": round(random.random(), 2), 
    #     "dl_cqi": round(random.random(), 2),
    #     "dl_brate": round(random.random(), 2), 
    #     "ul_bler": round(random.random(), 2), 
    #     "ul_mcs": round(random.random(), 2), 
    #     "ul_snr": round(random.random(), 2), 
    #     "ul_brate": round(random.random(), 2), 
    #     "ul_bsr": round(random.random(), 2), 
    #     "ul_phr": round(random.random(), 2), 
    #     "tx_gain": round(random.random(), 2), 
    #     "rx_gain": round(random.random(), 2), 
    #     "rnti": random.randint(1,3)
    # }

if __name__ == '__main__':
    sim = LTESimulator()
    sim.setPath("/kpilte")
    sim.start()

    try:
        while True:
            pass
    except:
        sim.stop_thread()
