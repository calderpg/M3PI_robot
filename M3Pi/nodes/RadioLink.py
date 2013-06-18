import serial
import time

class BASE_COMM_LINK():

    def __init__(self, serial_port, rate):
        self.port = serial.Serial(serial_port, rate, 8, 'N', 1, timeout=0.1)
        self.last_response = ""
        
    def Send(self, data):
        print "Writting " + data + " to the robot's serial port"
        self.port.write(data)
        time.sleep(0.1)
        reply_string = self.port.readline()
        print "Read " + reply_string + " from the robot's serial port"
        reply_chunks = reply_string.split("|")
        reply_data = reply_chunks[-1]
        self.last_response = reply_string
        return reply_data
        
    def GetResponse(self, function_code):
        cleaned_reply = self.last_response.lstrip("@")
        reply_chunks = cleaned_reply.split("|")
        reply_code = reply_chunks[2]
        reply_data = reply_chunks[3]
        if (reply_code.lower() == function_code):
            return float(reply_data)
        else:
            print "Eh, codes didn't match"
            return float(reply_dat)
