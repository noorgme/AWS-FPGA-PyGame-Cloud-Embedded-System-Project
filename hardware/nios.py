import numpy as np
import subprocess
import re
import binascii
from multiprocessing import Process, Pipe


# hex string to signed integer
def hexToInt(val:str) -> int:
    try:
        val = val.rjust(8,"0") #Pad hex to be 32 bits
        bite = binascii.unhexlify(val)
        return int.from_bytes(bite,byteorder='big', signed=True)
    except ValueError:
        return 0

def parseVector(text: str) -> np.ndarray:
    output = np.zeros((3))
    if len(re.findall("\[[0-9a-f]+,[0-9a-f]+,[0-9a-f]+\]", text)) == 0:
        return output
    text = text[1:]
    text = text[:-1]
    splt = text.split(",")
    for (i,val) in enumerate(splt):
        output[i] = hexToInt(val)
    return output


    
def processThread(conn:Pipe, process):
    while(1):
        vector = []
        for line in process.stdout:
            vector = parseVector(line.decode('utf-8').rstrip())
            if conn.recv():
                conn.send(vector)

class NiosConnector():
    
    def __init__(self):
        try:
            self._subprocess = subprocess.Popen(["~/intelFPGA_lite/22.1std/quartus/linux64/nios2-terminal"], shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
            self._parent_conn, self._child_conn = Pipe()
            self._process = Process(target=processThread, args = (self._child_conn, self._subprocess))
            self._process.start()
        finally:
            self._process.terminate()
            self._subprocess.terminate()

    def getVector(self) -> np.ndarray:
        self._parent_conn.send('a')
        return self._parent_conn.recv()
        
    
    def getRawOutput(self):
        raise NotImplementedError
