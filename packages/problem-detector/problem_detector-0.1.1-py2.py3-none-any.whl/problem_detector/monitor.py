from time import sleep
from datetime import datetime
import os
import getpass

import yaml
from log_aggregator_server.log_aggregator_server import log_aggregator

from .client import post_message, post_file
from .blackboard import BlackBoard


class Monitor(object):

    def __init__(self):
        self.blackboard = BlackBoard.get_instance()
        self.last_status = ""
        self.text = None
        self.log = None
        self.robot_uuid = getpass.getuser() + '@' + os.uname()[1]
        with open("config/config.yaml", 'r') as config_yaml:
            self.policy = yaml.load(config_yaml)
        self.mtr_status_policy = [mtr_status for mtr_status in self.policy.keys() if self.policy]

    def monitor(self):
        while not hasattr(self.blackboard, 'spinal_cord'): pass
        while hasattr(self.blackboard, 'spinal_cord'):
            current_status = self.get_status_from_spiral_cord()
            for mtr_status in self.mtr_status_policy:
                if current_status == mtr_status and current_status != self.last_status:
                    print('{} is detected!'.format(mtr_status))
                    if self.policy[mtr_status]['message'] and not self.policy[mtr_status]['log']:
                        post_message(message="{0} is {1}!".format(self.robot_uuid, mtr_status))
                    elif self.policy[mtr_status]['message'] and self.policy[mtr_status]['log']:
                        post_message(message="{0} is {1}!".format(self.robot_uuid, mtr_status))
                        post_message(message="Creating Log...")
                        tarfile = self.run_log_aggregator(mtr_status)
                        post_message(message="Uploading Log...")
                        post_file(file=open('/home/yujin/{}.tar.gz'.format(tarfile), 'rb'))
            self.last_status = current_status
            sleep(1)

    def get_status_from_spiral_cord(self):
        parsing_data = self.blackboard.spinal_cord
        parsing_list = parsing_data.split('\n')
        for i in parsing_list:
            parsing_index = i.rsplit()
            if parsing_index[0] == 'view_state':
                return parsing_index[2]

    def get_status_from_failure_detector(self):
        # Todo implement filtering failure status from failure detector blackboard
        pass

    @staticmethod
    def run_log_aggregator(status):
        tarfile_name = status + '_' + datetime.now().strftime("%Y%m%d%H%M%S")
        log_aggregator(tarfile_name)
        return tarfile_name
