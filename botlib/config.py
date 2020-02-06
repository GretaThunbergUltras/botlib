import json
import os

class ConfigSet(object):
    """
    A collection of configuration objects. Access via `bot.config()`.
    """
    
    DATA_DIR = '/usr/local/share/bot'
    CONFIG_DIR = os.path.join('/usr/local/share/bot', 'conf/')
    LOG_DIR = os.path.join('/usr/local/share/bot', 'log/')

    MOTOR_CONFIG = 'motors.json'
    STEER_PID_CONFIG = 'steer_pid.json'

    _motor = None
    _steer_pid = None

    def motor():
        """
        :return: an instance of `MotorConfig`
        """
        if ConfigSet._motor is None:
            ConfigSet._motor = MotorConfig()
        return ConfigSet._motor

    def steer_pid():
        """
        :return: an instance of `SteerPIDConfig`
        """
        if ConfigSet._steer_pid is None:
            ConfigSet._steer_pid = SteerPIDConfig()
        return ConfigSet._steer_pid

    def _get_file_path(fp: str):
        return os.path.join(ConfigSet.CONFIG_DIR, fp)

class Config(object):
    """
    Loads a configuration file `fname`. The file name must be relative to the default configuration directoy `ConfigSet.CONFIG_DIR` and must contain valid json.
    """
    def __init__(self, fname):
        if not os.path.exists(ConfigSet.CONFIG_DIR):
            os.makedirs(ConfigSet.CONFIG_DIR)

        self._fname = fname
        self._path = ConfigSet._get_file_path(self._fname)
        self._data = self._load()

    def __getitem__(self, name):
        name = str(name)
        if name not in self._data:
            return None
        return self._data[name]

    def __setitem__(self, name, value):
        name = str(name)
        self._data[name] = value
        self._save()

    def _bootstrap(self):
        """
        Called when the configuration file is initialized inside the filesystem.

        :return: either `dict` with the default key-value-pairs or `None`
        """
        return None

    def _save(self):
        with open(self._path, 'w') as f:
            f.write(json.dumps(self._data))

    def _load(self):
        if not os.path.exists(self._path):
            print('config {} not found, creating'.format(self._path))
            boot = self._bootstrap()
            self._data = {} if boot is None else boot
            self._save()

        with open(self._path, 'r') as f:
            raw = f.read()
            return json.loads(raw)
        
        return {}

class MotorConfig(Config):
    """
    Stores the minimum, maximum and default position for calibrated motors. Access via `bot.config().motor()`.
    """
    def __init__(self):
        super().__init__(ConfigSet.MOTOR_CONFIG)

class SteerPIDConfig(Config):
    """
    Stores the PID controller values for steering. Access via `bot.config().steer_pid()`.
    """
    def __init__(self):
        super().__init__(ConfigSet.STEER_PID_CONFIG)

    def _bootstrap(self):
        return { 'cp': 85, 'p': 1.8, 'i': 0.002, 'd': 0.6 }
