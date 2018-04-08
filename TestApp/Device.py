
import serial
import serial.tools.list_ports as portlist

class USBduino():
    def __init__(self):
        pass

    def open(self, pid, vid, baud):
        """
        Opens serial connection to the arduino.
        """
        portname = self.find_port(vid, pid)

        self.port = serial.Serial(portname, baud)

    def find_port(self, vid, pid):
        """
        Finds the port name for the desired device.
        """

        ports = portlist.comports()
        for port in portlist:
            if port.vid == vid and port.pid == pid:
                return port.device
        return None

    def close(self):
        """
        Closes the arduino port
        """
        self.port.close()

    def record(self):
        """
        signal the arduino to begin relaying data
        signal is "r\n"
        """
        str = "r\n".encode('ascii')
        self.port.write(str)

    def standby(self):
        """
        tell the arduino to standby (stop sending data)
        signal is "s\n"
        """
        str = "s\n".encode('ascii')
        self.port.write(str)

    def imu_calibrate(self):
        """
        signal the arduino to calibrate its IMU
        signal is simple "c\n".
        """
        str = "c\n".encode('ascii')
        self.port.write(str)


    def poll(self):
        """
        poll the arduino's serial port for new data. When new data arrives, build up
        a data string until a newline is reached. At this point, send the data to the appmodel
        """
        while True:

            time.sleep(100)
            str = ""

            #iterate while the port buffer has data
            while not self.port.in_waiting() == 0:
                #build up a string with each new character
                nchar = self.port.read()
                nchar.encode('utf-8')
                if nchar == '\n':
                    #save string
                    break
                else:
                    str += nchar


class BLEduino():
    """
    class to handle bluetooth communication.
    """
    def __init__(self):
        pass

    def open(self, pid, vid, baud):
        """
        Opens serial connection to the arduino.
        """
        pass

    def close(self):
        """
        Closes the arduino port
        """
        pass

    def record(self):
        """
        signal the arduino to begin relaying data
        """
        pass

    def standby(self):
        """
        tell the arduino to standby (stop sending data)
        """
        pass

    def imu_calibrate(self):
        """
        signal the arduino to calibrate its IMU
        """
        pass

    def poll(self):
        """
        poll the arduino serial port for new data. When new data arrives, build up
        a data string until a newline is reached. At this point, send the data to the appmodel
        """
