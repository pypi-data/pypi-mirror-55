# -*- coding: utf-8 -*-

"""Main module."""
import threading

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
        self.sc_thread.start()
        self.monitor_thread.start()

    def shutdown(self):
        self.callback_instance.shutdown()