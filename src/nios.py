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


def readThread(subproc, q):
    while 1:
        line = subproc.readline()
        if(line != ''):
            print(line)
            q.put(line)


class NiosConnector():
        
    def __init__(self):
        try: 
            # ===TEMP STUFF BECAUSE MY QUARTUS INSTALL IS MESSED UP =======
            d = dict(os.environ)
            # d['PATH'] = d['PATH']+":/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
            # d['LD_LIBRARY_PATH'] = "/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
            #os.environ['LD_LIBRARY_PATH'] = d['LD_LIBRARY_PATH']+"/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
            
            self._niosBridge = intel_jtag_uart.intel_jtag_uart()
            # ===========
            # self._subprocess = subprocess.Popen(["~/intelFPGA_lite/22.1std/quartus/linux64/nios2-terminal"], 
            #                                     shell=True, 
            #                                     env=d,
            #                                     executable="/bin/bash", 
            #                                     stdin=subprocess.PIPE, 
            #                                     stdout=subprocess.PIPE, 
            #                                     encoding='utf-8',
            #                                     universal_newlines=True
            #                                 )
            # self._readQueue = mp.Queue()
            # self._readThread = mp.Process(target=readThread, args = (self._subprocess.stdout,self._readQueue))
            # self._readThread.daemon = True
            # self._readThread.start()
            
        except Exception as e:
            try:
                # self._subprocess.terminate()
                None
            except AttributeError: # If _subprocess haven't been assigned yet.
                None
            raise e
        finally:
            # self._subprocess.terminate()
            None

    def getVector(self) -> np.ndarray:
        self._niosBridge.write(b'V')
        return self._parseVector(self._niosBridge.read().decode().rstrip())


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
        return output
    
    def close(self):
        self._subprocess.terminate()
        
        
# Testing code
if __name__ == "__main__":
    controller = NiosConnector()
    fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
    plt.ion()
    plt.show()
    while 1:
        vector = controller.getVector()
        ax.clear()
        ax.quiver([0],[0],[0],[vector[0]],[vector[1]],[vector[2]])
        #print("Vector", vector)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.draw()
        plt.pause(0.0001)