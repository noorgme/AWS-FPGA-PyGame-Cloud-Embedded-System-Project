import numpy as np
import subprocess
import re
import binascii
from multiprocessing import Process, Array
import os,  time


class NiosConnector():
        
    def __init__(self):
        try: 
            d = dict(os.environ)
            d['PATH'] = d['PATH']+":/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
            d['LD_LIBRARY_PATH'] = "/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
            self._subprocess = subprocess.Popen(["~/intelFPGA_lite/22.1std/quartus/linux64/nios2-terminal"], shell=True,env=d, executable="/bin/bash",stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            
        except Exception as e:
            try:
                self._subprocess.terminate()
            except AttributeError: # If _process or subprocess haven't been assigned yet.
                None
            raise e
        finally:
            self._subprocess.terminate()

    def getVector(self) -> np.ndarray:
        try:
            self._subprocess.stdin.write('L'.encode('utf-8') + b'\n')
            l = ""
            print(self._subprocess.stdout.read())
            time.sleep(0.001)
                
            return 0
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