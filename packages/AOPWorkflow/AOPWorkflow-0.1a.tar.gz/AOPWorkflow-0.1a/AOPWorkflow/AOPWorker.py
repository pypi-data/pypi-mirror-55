class AOPWorker():
    def __init__(self, work_function):
        self._work_function = work_function

    def work(self, context):
        return self._work_function(context)
