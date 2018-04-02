class DataQueue():
    """
    Dataqueue works like a FIFO queue, but is size limited. Enqueueing data such
    that there are more datapoints than maxsize will automatically trigger a dequeue
    operation such that the length is constant
    """
    def __init__(self, msize):
        self.data = []
        self.maxsize = msize
        self.size = len(self.data)

    def enqueue(self, element):
        """
        Tacks a new element onto the back of the queue
        """
        self.data.append(element)
        self.size += 1
        #if the
        if self.size > self.maxsize:
            self.dequeue()

    def dequeue(self):
        """
        Removes and element from the front of the queue
        """
        self.data.pop(0)
        self.size -= 1

    def get_size(self):
        return self.size

    def get_data(self):
        return self.data

    def set_size(self, nsize):
        self.size = nsize

    def set_data(self, ndata, msize):
        self.data = ndata
        self.maxsize = msize
