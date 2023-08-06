# -*- coding: utf-8 -*-

"""Main module."""
import threading
import os

import yaml

from .blackboard import BlackBoard
from .supervisor import Supervisor
try:
    from .collector.status_collector import StatusCollector
    ros_found = True
except ModuleNotFoundError:
    print('ROS is not founded.')
    ros_found = False


class ProblemDetector(object):

    def __init__(self):
        self.blackboard = BlackBoard.get_instance()

        if ros_found:
            self.status_collector_instance = StatusCollector()
            self.status_collector_thread = threading.Thread(target=self.status_collector_instance.main)
            self.status_collector_thread.daemon = True
        self.supervisor_instance = Supervisor()
        self.supervisor_thread = threading.Thread(target=self.supervisor_instance.main)
        self.supervisor_thread.daemon = True

    def setup(self):
        # config setup
        pkg_path = os.path.dirname(__file__)
        config_path = os.path.join(pkg_path, 'config')
        config_list = os.listdir(config_path)

        for config_file in config_list:
            config_file_path = os.path.join(config_path, config_file)
            with open(config_file_path, 'r') as config_yaml:
                config = yaml.safe_load(config_yaml)
            parameter = os.path.splitext(config_file)[0]
            self.blackboard.add_attr(parameter, config)

        self.status_collector_instance.setup()
        self.supervisor_instance.setup()

    def main(self):
        config_data = self.blackboard.get_attr()
        print('\033[1m---------- CONFIG CONTENTS ----------\033[0m')
        print(yaml.safe_dump(config_data))

        if ros_found:
            self.status_collector_thread.start()
        self.supervisor_thread.start()

    def shutdown(self):
        self.status_collector_instance.shutdown()
