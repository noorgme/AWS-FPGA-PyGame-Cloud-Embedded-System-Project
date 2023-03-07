import time
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import math, re, os
import binascii

# hex string to signed integer
def hexToInt(val:str) -> int:
    try:
        val = val.rjust(8,"0") #Pad hex to be 32 bits
        #print(val)
        bite = binascii.unhexlify(val)
        return int.from_bytes(bite,byteorder='big', signed=True)
    except ValueError:
        return 0

def parseVector(text: str) -> np.ndarray:
    #print(text)
    output = np.zeros((3))
    if len(re.findall("\[[0-9a-f]+,[0-9a-f]+,[0-9a-f]+\]", text)) == 0:
        return output
    text = text[1:]
    text = text[:-1]
    splt = text.split(",")
    for (i,val) in enumerate(splt):
        output[i] = hexToInt(val)
    return output


fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
plt.ion()
plt.show()
d = dict(os.environ)
d['PATH'] = d['PATH']+":/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
d['LD_LIBRARY_PATH'] = "/home/harry/intelFPGA_lite/22.1std/quartus/linux64/"
NiosProc = subprocess.Popen(["~/intelFPGA_lite/22.1std/quartus/linux64/nios2-terminal"], shell=True,executable="/bin/bash", stdout=subprocess.PIPE, env=d)

try:
    while(1):
        vector = [0,0,0]
        for line in NiosProc.stdout:
            vector = parseVector(line.decode('utf-8').rstrip())
            ax.clear()
            ax.quiver([0],[0],[0],[vector[0]],[vector[1]],[vector[2]])
            #print("Vector", vector)
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.draw()
            plt.pause(0.0001)

finally:
    NiosProc.terminate()