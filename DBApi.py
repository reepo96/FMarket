import abc
class DBApi(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def createtable(self, tabname):
        pass

    @abc.abstractmethod
    def savebar(self, productid, barlevel, barlist):
        pass

    @abc.abstractmethod
    def getbar(self, productid, instrumentid, freq, beginMin, endMin):
        pass


