from nios import NiosConnector
import time

controller = NiosConnector()

while 1:
    print(controller.getVector())
    time.sleep(1)