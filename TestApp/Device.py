"""
Collin - Merge yer code here, but use the interface defined in the BLEduino class.
Make sure all the skeleton methods stay there even if you don't implement themself.
                ----I wish python had real interfaces like java----


Why? I basically want these two classes to work interchangably like python variables
We can pop between the two modes of communication 
"""
import pyserial

class USBduino():
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
