# -*- coding: utf-8 -*-

"""Main module."""
import rospy
from std_msgs.msg import String

from problem_detector.blackboard import BlackBoard


class StatusCollector(object):

    def __init__(self):
        self.blackboard = BlackBoard.get_instance()
        self.spinal_cord_sc = None

    def setup(self):
        self.blackboard.add_attr('status', '')

    def main(self):
        self.spinal_cord_sc = rospy.Subscriber('/gopher_spinal_cord/blackboard', String, self.spinal_cord_callback)

    def shutdown(self):
        self.spinal_cord_sc.unregister()

    def spinal_cord_callback(self, data):
        """
        /gopher_spinal_cord/blackboard = robot's status
        :param data:
        :return:
        """
        status = self.get_status_from_spiral_cord(str(data))
        self.blackboard.status = status

    @staticmethod
    def get_status_from_spiral_cord(spinal_cord_data):
        parsing_list = spinal_cord_data.split('\n')
        for i in parsing_list:
            parsing_index = i.rsplit()
            if parsing_index[0] == 'view_state':
                return parsing_index[2]
