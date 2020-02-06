from datetime import datetime

class LogInput(object):
    def __init__(self, log):
        self._log = log
        self._last = datetime.now()

    def _init(self, **kwargs):
        self._log.update(0, **kwargs)

    def _update(self, **kwargs):
        now = datetime.now()
        self._log.update(now - self._last, **kwargs)
        self._last = now

class LogMotor(LogInput):
    def __init__(self, log, port):
        super().__init__(log)
        self._port = port
        self._init(ty='change_power', port=self._port, value=0)

    def change_power(self, nv):
        self._update(ty='change_power', port=self._port, value=nv)

    def change_position(self, nv):
        self._update(ty='change_position', port=self._port, value=nv)

    def change_position_factor(self, nv):
        self._update(ty='change_position_factor', port=self._port, value=nv)

class Log(object):
    def __init__(self):
        pass

    def update(self, td, **kwargs):
        print('[LOG]', td, kwargs)

    def new_motor(self, port) -> LogInput:
        return LogMotor(self, port)
