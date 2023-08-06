from AOPException import AOPException
class AOPRunner():
    _workers = None
    _terminal = lambda self,ctx: print("Workflow ends with", ctx)

    def __init__(self, workers):
        self._workers = workers

    def setTerminal(self, terminal):
        self._terminal = terminal

    def run(self, context):
        ctx = context
        index_exec = 0
        try:
            for node in self._workers:
                ctx = node.work(ctx)
                index_exec += 1
        except Exception as e:
            raise AOPException(index_exec, e)
        self._terminal(ctx)
