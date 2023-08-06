from time import sleep
from datetime import datetime
import os
import getpass

from log_aggregator_server.log_aggregator_server import log_aggregator

from .detector import *
from .client import Client
from .blackboard import BlackBoard


class Supervisor(object):

    def __init__(self):
        self.blackboard = BlackBoard.get_instance()
        self.robot_uuid = getpass.getuser() + '@' + os.uname()[1]
        self.detector_list = []
        self.status_observer = status_detector.StatusDetector()
        self.client = Client()

    def setup(self):
        self.status_observer.setup()
        self.detector_list.append(self.status_observer)

    def main(self):
        while True:
            for detector in self.detector_list:
                detect_result = detector.detect()
                if detect_result['detect']:
                    if detect_result['message']:
                        self.client.post_message(self.robot_uuid + '\t' + detect_result['message'])
                    if detect_result['log']:
                        self.client.post_message('Creating log file...')
                        filename = self.run_log_aggregator(detect_result['topic'])
                        self.client.post_message('Uploading log file...')
                        self.client.post_file(
                            file=open(os.path.join('/home', getpass.getuser(), filename + '.tar.gz'), 'rb'))
            sleep(1)

    def run_log_aggregator(self, status):
        tarfile_name = self.robot_uuid + '_' + status + '_' + datetime.now().strftime("%Y%m%d%H%M%S")
        log_aggregator(tarfile_name)
        return tarfile_name
