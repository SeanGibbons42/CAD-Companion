import sys
sys.path.append("..\\")

from TestApp.Models import AppModel, DataQueue

class TestModels():
    def cyka(self):
        return 2+2

    def test_cyka(self):
        assert self.cyka() == 4

    def test_parsing(self):
        #Run the function and get the results:
        model = AppModel(10)
        model.parse_data("100A10#10#10#G20#20#20#")
        result_1 = {k:v.peek_head() for k,v in model.queues.items()}

        #Set up a test case
        testkeys = ["time","ax", "ay", "az", "gx", "gy", "gz", "gnet", "anet"]
        testvalues = [100, 10, 10, 10, 20, 20, 20, (3*20**2)**0.5, (3*10**2)**0.5 ]
        testdict = dict(zip(testkeys, testvalues))

        assert result_1 == testdict
