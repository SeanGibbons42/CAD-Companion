import serial
import queue
import serial.tools.list_ports as portlist
from tkinter import messagebox

class USBduino():
    def __init__(self, app):
        self.outbox = queue.Queue()
        self.rec = False
        self.appmod = app

    def open(self, pid, vid, baud):
        """
        Opens serial connection to the arduino.
        Returns: port - serial instance pointing the desired port
                      - (= None if port not found)
        """

        portname = self.find_port(vid, pid)
        if portname is None:
            messagebox.showwarning("Error","Invalid Port #")
            return None

        self.port = serial.Serial(portname, baud)

        return self.port

    def find_port(self, vid, pid):
        """
        Finds the port name for the desired device.
        """

        ports = portlist.comports()
        for port in ports:
            if port.vid == vid and port.pid == pid:
                return port.device
        return None

    def write_cmd(self, cmd):
        cmd = cmd.encode('ascii')
        self.port.write(cmd)

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
        self.rec = True

    def standby(self):
        """
        tell the arduino to standby (stop sending data)
        signal is "s\n"
        """
        str = "s\n".encode('ascii')
        self.port.write(str)
        self.rec = False

    def imu_calibrate(self):
        """
        signal the arduino to calibrate its IMU
        signal is simple "c\n".
        """
        str = "c\n".encode('ascii')
        self.port.write(str)

    def poll_outbox(self):
        """
        Poll the outgoing messagebox, and send messages immediately if:
            1) We aren't expecting incoming messages: 802.15.4 is half-duplex (can transmit OR recieve at a time)
            2) There is a message waiting
        """
        while True:
            time.sleep(100)
            if not self.rec and not self.outbox.empty():
                #send the command if the conditions are met
                self.write_cmd(self.outbox.dequeue())

    def poll_device(self):
        """
        poll the arduino's serial port for new data. When new data arrives, build up
        a data string until a newline is reached. At this point, send the data to the appmodel
        """
        str = ""
        while True:
            time.sleep(100)

            #iterate while the port buffer has data
            while not self.port.in_waiting() == 0:
                #build up a string with each new character
                nchar = self.port.read()
                nchar.encode('utf-8')
                if nchar == '\n':
                    if self.rec == True:
                        #send the next available message
                        self.port.write(outbox.dequeue())

                    #save the data and reset the command buffer string
                    self.appmod.parse_data(str)
                    str = ""

                else:
                    str += nchar
