import numpy as np
import subprocess
import re
import binascii
import threading, queue
import os,  time



def readThread(subproc, q):
    print(subproc.poll())
    while subproc.poll() is None:
        for line in subproc.stdout.readlines():
            if(line != ''):
                print(line)
                q.put(line)


class NiosConnector():
        
    def __init__(self):
        try: 
            d = dict(os.environ)
            d['PATH'] = d['PATH']+":/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
            d['LD_LIBRARY_PATH'] = "/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
            self._subprocess = subprocess.Popen(["~/intelFPGA_lite/22.1std/quartus/linux64/nios2-terminal"], shell=True,env=d, executable="/bin/bash", stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
            self._readQueue = queue.Queue()
            self._readThread = threading.Thread(target=readThread, args = (self._subprocess,self._readQueue))
            self._readThread.daemon = True
            self._readThread.start()
        except Exception as e:
            try:
                self._subprocess.terminate()
            except AttributeError: # If _subprocess haven't been assigned yet.
                None
            raise e
        finally:
            self._subprocess.terminate()

    def getVector(self) -> np.ndarray:
        try:
            self._subprocess.stdin.write('V')
            return self._parseVector(self._readQueue.get())
        except TimeoutError:
            raise TimeoutError("NIOS COMMUNICATION TIMEOUT!!")

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