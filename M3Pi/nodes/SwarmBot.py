class SWARMBOT():

    def __init__(self, ID_string, comm_link):
        self.ID = ID_string
        self.RadioLink = comm_link
        self.Reset()
        self.maxturn = 1.0
        
    def Reset(self):
        """stuff"""
        pass
        
    def Car_Drive(self, speed, turn):
        """stuff"""
        if ((speed == 0.0 or speed == -0.0) and turn < 0.0):
            self.Tank_Drive(abs(turn), -abs(turn))
        elif ((speed == 0.0 or speed == -0.0) and turn > 0.0):
            self.Tank_Drive(-abs(turn), abs(turn))
        elif (speed > 0.0 and turn > 0.0):
            left = speed * (1 - (abs(turn) / self.maxturn))
            right = speed
            self.Tank_Drive(left, right)
        elif (speed > 0.0 and turn < -0.0):
            left = speed
            right = speed * (1 - (abs(turn) / self.maxturn))
            self.Tank_Drive(left, right)
        elif (speed < -0.0 and turn > 0.0):
            left = speed * (1 - (abs(turn) / self.maxturn))
            right = speed
            self.Tank_Drive(left, right)
        elif (speed < -0.0 and turn < -0.0):
            left = speed
            right = speed * (1 - (abs(turn) / self.maxturn))
            self.Tank_Drive(left, right)
            
    def Sanitize(self, left, right):
        return_values = [left, right]
        if (left > 1.0):
            return_values[0] = 1.0
        elif (right > 1.0):
            return_values[1] = 1.0
        elif (left < -1.0):
            return_values[0] = -1.0
        elif (right < -1.0):
            return_values[1] = -1.0
        return return_values
        
    def Tank_Drive(self, left, right):
        """stuff"""
        cleaned_values = self.Sanitize(left, right)
        self.RadioLink.Send("$-1|0|d|" + str(cleaned_values[0]) + "|" + str(cleaned_values[1]) + "|0.0|0.0\n")
        
    def Stop(self):
        """stuff"""
        self.Tank_Drive(0.0, 0.0)
        
    def GetDistance(self):
        """stuff"""
        self.RadioLink.Send("$-1|0|m|0.0|0.0|0.0|0.0\n")
        measured_value = self.RadioLink.GetResponse("m")
        return self.EstimatedDistance(measured_value)
        
    def EstimatedDistance(self, raw_sensor_value):
        raw_voltage = 3.3 * raw_sensor_value
        avg_min_voltage = 0.45
        avg_max_voltage = 2.75
        if (raw_voltage > 2.5):
            return 15.0
        elif (raw_voltage > 2.1):
            return 20.0
        elif (raw_voltage > 1.7):
            return 30.0
        elif (raw_voltage > 1.4):
            return 40.0
        elif (raw_voltage > 1.2):
            return 50.0
        elif (raw_voltage > 0.9):
            return 60.0
        elif (raw_voltage > 0.8):
            return 70.0
        elif (raw_voltage > 0.7):
            return 80.0
        elif (raw_voltage > 0.6):
            return 90.0
        else:
            return 100.0
        
    def SetLEDs(self, led1, led2, led3, led4, led5, led6, led7, led8):
        """stuff"""
        print "Not currently implemented, sorry"
        
    def GetBattery(self):
        """stuff"""
        self.RadioLink.Send("$-1|0|b|0.0|0.0|0.0|0.0\n")
        measured_value = self.RadioLink.GetResponse("b")
        
    def SetLCD(self, display_string):
        """stuff"""
        print "Not currently implemented, sorry"
        
