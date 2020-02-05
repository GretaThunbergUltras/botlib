import json
import os

class Config(object):
    CONFIG_DIR = '/home/pi/botconf'
    MOTOR_CONFIG = 'motors.json'
    STEER_PID_CONFIG = 'steer_pid.json'

    def __init__(self, path=None):
        if not os.path.exists(Config.CONFIG_DIR):
            os.mkdir(Config.CONFIG_DIR)
        
        self._motor_config = self._load_config(Config.MOTOR_CONFIG)

    def _get_file_path(self, fp: str):
        return os.path.join(Config.CONFIG_DIR, fp)

    def _save_config(self, path, config):
        path = self._get_file_path(path)
        with open(path, 'w') as f:
            f.write(json.dumps(config))

    def _load_config(self, path):
        path = self._get_file_path(path)

        if not os.path.exists(path):
            print('config not found, creating')
            self._save_config(path, {})

        with open(path, 'r') as f:
            raw = f.read()
            return json.loads(raw)
        
        return {}

    def motor_config(self, port):
        port = str(port)
        if port not in self._motor_config:
            return None
        return self._motor_config[port]

    def set_motor_config(self, port, config):
        port = str(port)
        self._motor_config[port] = config
        self._save_config(Config.MOTOR_CONFIG, self._motor_config)
