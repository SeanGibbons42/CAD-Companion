class AppModel():
    def __init__(self, bsize):
        self.buffer_size = buffer_size

        self.ax_queue = DataQueue(b_size)
        self.ay_queue = DataQueue(b_size)
        self.az_queue = DataQueue(b_size)

        self.gx_queue = DataQueue(b_size)
        self.gy_queue = DataQueue(b_size)
        self.gz_queue = DataQueue(b_size)

        self.gnet_queue = DataQueue(b_size)
        self.anet_queue = DataQueue(b_size)

        self.time_queue = DataQueue(b_size)

    def parse_data(self, data):
        """
        Parses raw gyro data and sends it to the data queues

        Format: <Time>A<Ax>#<Ay>#<Az>#G<Gx>#<Gy>#<Gz>#
        """
        #first, get the timestamp
        old_ind = 0
        n_ind = data.index('A')
        self.time_queue.enqueue( float(data[old_ind:n_ind]) )
        #next, grab the three accelerometer measurementsd
        for i in range(3):
            old_ind = n_ind + 1
            a.append(float(data[old_ind:n_ind]))
        #third, we need to get the gyro values
        n_ind += 1
        for i in range(3):
            old_ind = n_ind + 1
            g.append(float(data[old_ind:n_ind]))
        #place the datapoints into the appropriate queue
        self.ax_queue.enqueue(a[0]); self.ay_queue.enqueue(a[1]); self.az.enqueue(a[2])
        self.gx_queue.enqueue(g[0]); self.gy_queue.enqueue(g[1]); self.gz.enqueue(g[2])

        self.anet_queue.enqueue(self.norm(a))
        self.gnet_queue.enqueue(self.norm(g))

    def norm(self, vec):
        """
        Computes the two-norm of a vector (returns its magnitude). Works for n-dimensional
        vectors.
        """
        sum = 0

        for comp in vec:
            sum += comp**2

        return sum**0.5


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
