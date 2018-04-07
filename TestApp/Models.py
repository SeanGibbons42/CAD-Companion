class AppModel():
    def __init__(self, bsize):
        self.buffer_size = bsize
        self.queues = {
            "time":DataQueue(bsize),

            "ax":DataQueue(bsize),
            "ay":DataQueue(bsize),
            "az":DataQueue(bsize),

            "gx":DataQueue(bsize),
            "gy":DataQueue(bsize),
            "gz":DataQueue(bsize),

            "gnet":DataQueue(bsize),
            "anet":DataQueue(bsize)
        }


    def parse_data(self, data):
        """
        Parses raw gyro data and sends it to the data queues
        Format: <Time>A<Ax>#<Ay>#<Az>#G<Gx>#<Gy>#<Gz>#
        """
        a = []
        g = []

        #first, get the timestamp for the measurement
        old_ind = 0
        n_ind = data.index('A')
        self.queues['time'].enqueue( float(data[old_ind:n_ind]) )

        #next, grab the three accelerometer measurements
        for i in range(3):
            old_ind = n_ind + 1
            n_ind = data.index('#', old_ind)
            a.append(float(data[old_ind:n_ind]))
            
        #third, we need to get the gyro values
        n_ind += 1
        for i in range(3):
            old_ind = n_ind + 1
            n_ind = data.index('#', old_ind)
            g.append(float(data[old_ind:n_ind]))

        #place the datapoints into the appropriate queue
        self.queues['ax'].enqueue(a[0]); self.queues['ay'].enqueue(a[1]); self.queues['az'].enqueue(a[2])
        self.queues['gx'].enqueue(g[0]); self.queues['gy'].enqueue(g[1]); self.queues['gz'].enqueue(g[2])

        self.queues['anet'].enqueue(self.norm(a))
        self.queues['gnet'].enqueue(self.norm(g))

    def norm(self, vec):
        """
        Computes the two-norm of a vector (returns its magnitude). Works for n-dimensional
        vectors.
        """
        sum = 0
        #sum the squares of the components
        for component in vec:
            sum += component**2

        #return the sqrt of the sum
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
        Removes and element from the front of the queue.
        Accepts - nothing
        """
        self.data.pop(0)
        self.size -= 1

    def get_size(self):
        return self.size

    def get_data(self):
        return self.data

    def set_size(self, nsize):
        """
        Set the maximum length of the arrayself.
        Accepts: integer nsize: the new max size
        Returns: None
        """
        self.size = nsize

    def set_data(self, ndata, msize):
        """
        Set the contents of the queue to be the elements of a list. Also requires
        that a new max size of the array to be specified.
        Accepts: list ndata - new data
                 integer msize - new max size
        """
        self.data = ndata
        self.maxsize = msize

    def peek_head(self):
        """
        Return the FI (first in element).
        Accepts - nothing
        Returns - <any type> data: current FI datapoint
        """
        return self.data[0]

    def peek_tail(self):
        """
        Returns the LI (last in element.)
        Returns: - <any type> data: current LI datapoint
        """
        return self.data[-1]
