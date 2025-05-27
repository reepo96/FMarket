import zmq
import json

class BarPub:
    def __init__(self):
        self.context = zmq.Context()
        self.puber = self.context.socket(zmq.PUB)
        self.puber.bind("tcp://127.0.0.1:13356")

    def senddata(self,  bardata):
        bar_byte = bytes('{}'.format(bardata),'utf-8')
        self.puber.send(bar_byte)

    def send_tickdata(self,tickdata):
        tickdata["DataType"] = "tickdata"
        tickdata_byte = bytes('{}'.format(tickdata), 'utf-8')
        self.puber.send(tickdata_byte)
