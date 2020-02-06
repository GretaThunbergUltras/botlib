from threading import Thread
from queue import Empty, PriorityQueue

class Terminate:
    pass

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

    def join(self):
        """
        Wait for the `Task` to finish.
        """
        self._thread.join()

class WorkerTask:
    def __init__(self, tickfn=None):
        self._thread = Thread(group=None, target=self._entry, daemon=True)
        self._queue = PriorityQueue()
        self._running = True
        self._tickfn = tickfn

    def start(self):
        self._thread.start()

    def send_message(self, evt):
        prio = 0
        if isinstance(evt, Terminate):
            prio += 1
        self._queue.put((prio, evt))

    def tick(self, evt=None):
        if not self._tickfn is None:
            self._tickfn(evt)

    def _stop(self):
        self._running = False

    def _entry(self):
        while self._running:
            try:
                _prio, evt = self._queue.get_nowait()
            except Empty:

                self.tick()

                continue

            if isinstance(evt, Terminate):
                self.stop()
                break

            self.tick(evt)
