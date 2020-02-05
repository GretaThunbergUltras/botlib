from threading import Thread

class Task:
    def __init__(self, func, daemon=True):
        """
        A slim wrapper for running functions in background.

        :param func: a callable to execute
        :param daemon: do not wait for this `Task` to finish defaults to `True`.
        """
        self._thread = Thread(group=None, target=func, daemon=daemon)

    def start(self):
        """
        Start the `Task`.
        """
        self._thread.start()
