import numpy as np
import subprocess
import re
import binascii
import threading, queue
import os,  time
import time
from subprocess import Popen
import multiprocessing as mp
import intel_jtag_uart
import matplotlib.pyplot as plt

THRESHOLD = 100


class NiosConnector():
        
    def __init__(self):
        try: 
            self._niosBridge = intel_jtag_uart.intel_jtag_uart()
            self._hasBomb = False
            self._ledsLit = False
            self.setLEDS(False)
            self.setBomb(False)
        except Exception as e:
            if str(e) == "Cable not available":
                print("CONTROLLER NOT CONNECTED!!")
                self._niosBridge = None
            if str(e) == "Another program is already using the UART":
                print("CONTROLLER ALREADY CONNECTED!!")
                self._niosBridge = None
            else:
                self._niosBridge.close()
                raise e

    def getVector(self) -> np.ndarray:
        self._niosBridge.write(b'V')
        return self._parseVector(self._niosBridge.read().decode().rstrip())
    
    def getDirection(self) -> int:
        if self._niosBridge is None:
            return 0
        vec = self.getVector()
        if(vec[0] > THRESHOLD):
            return 1
        elif(vec[0] < -THRESHOLD):
            return -1
        return 0
    
    def setLEDS(self,on:bool):
        if on != self._ledsLit:
            self._ledsLit = on
            if(on):
                self._niosBridge.write(b'L')
            else:
                self._niosBridge.write(b'l')
            self._niosBridge.read()
    
    def setBomb(self, on:bool):
        if on != self._hasBomb:
            self._hasBomb = on
            if(on):
                self._niosBridge.write(b'B')
            else:
                self._niosBridge.write(b'b')
            self._niosBridge.read()

    # hex string to signed integer
    def _hexToInt(self, val:str) -> int:
        try:
            val = val.rjust(8,"0") #Pad hex to be 32 bits
            bite = binascii.unhexlify(val)
            return int.from_bytes(bite,byteorder='big', signed=True)
        except ValueError:
            return 0

    def _parseVector(self, text: str) -> np.ndarray:
        output = np.zeros((3))
        if len(re.findall("\[[0-9a-f]+,[0-9a-f]+,[0-9a-f]+\]", text)) == 0:
            return output
        text = text[1:]
        text = text[:-1]
        splt = text.split(",")
        for (i,val) in enumerate(splt):
            output[i] = self._hexToInt(val)
        #FIXME: FIGURE OUT WHY THE Z AXIS IS SO BAD
        output[2] = 0 #Z axis is messed up so set it to 0
        return output
    
    def close(self):
        self._niosBridge.close()
        
        
# Testing code
if __name__ == "__main__":
    controller = NiosConnector()
    controller.setLEDS(True)
    # plt.figure(0)
    # fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    # ax.axes.set_xlim3d(left=-200.0,right=200.0)
    # ax.axes.set_ylim3d(bottom=-200.0,top=200.0)
    # ax.axes.set_zlim3d(bottom=-200.0,top=200.0)
    # plt.figure(1)
    # fig2, ax2 = plt.subplots(3,1)
    # ax2[0].set_title("Accel X")
    # ax2[1].set_title("Accel Y")
    # ax2[2].set_title("Accel Z")
    # plt.ion()
    # plt.show()
    # i=0
    # while 1:
    #     vector = controller.getVector()
    #     ax.clear()
    #     ax.quiver([0],[0],[0],[vector[0]/300],[vector[1]/300],[0])  
    #     if i >= 1000:
    #         ax2[0].clear()
    #         ax2[1].clear()
    #         ax2[2].clear()
    #         i=0
    #     ax2[0].plot(i,vector[0],'o',color="green")
    #     ax2[1].plot(i,vector[1],'o',color="blue")
    #     ax2[2].plot(i,0,'o',color="red")
    #     i+=1
    #     #print("Vector", vector)
    #     fig.canvas.draw()
    #     fig.canvas.flush_events()
    #     fig2.canvas.draw()
    #     fig2.canvas.flush_events()
    #     plt.draw()
    #     plt.pause(0.0000001)
    while 1:
        dirMap = ["NONE","RIGHT","LEFT"]
        print(dirMap[controller.getDirection()])