# -*- coding: utf-8 -*-

"""Main module."""
import threading
import os

import yaml

from .monitor import Monitor
from .callback import Callback


class ProblemDetector(object):

    def __init__(self):
        self.callback_instance = Callback()
        self.monitor_instance = Monitor()
        self.sc_thread = threading.Thread(target=self.callback_instance.setup)
        self.monitor_thread = threading.Thread(target=self.monitor_instance.monitor)
        self.sc_thread.daemon = True
        self.monitor_thread.daemon = True

    def main(self):
        pkg_path = os.path.dirname(__file__)
        for config in ['server_config', 'policy_config']:
            server_config_file_path = os.path.join(pkg_path, 'config/{}.yaml'.format(config))
            with open(server_config_file_path, 'r') as config_file:
                config_content = yaml.safe_load(config_file)
            print('\033[1m----- {} Contents -----\033[0m'.format(config.upper()))
            print(yaml.safe_dump(config_content))
        self.sc_thread.start()
        self.monitor_thread.start()

    def shutdown(self):
        self.callback_instance.shutdown()