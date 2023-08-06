class AOPException(Exception):
    def __init__(self, ind, excpt):
        self.index = ind
        self.exception = excpt
    
    def __str__(self):
        return "Error at function #{}: {}".format(self.index, self.exception)