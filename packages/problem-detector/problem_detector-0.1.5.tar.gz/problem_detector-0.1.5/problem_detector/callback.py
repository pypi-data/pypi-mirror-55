# -*- coding: utf-8 -*-

"""Main module."""
import rospy
from std_msgs.msg import String

from .blackboard import BlackBoard


class Callback(object):

    def __init__(self):
        self.blackboard = BlackBoard.get_instance()
        self.pose_sc = None
        self.spinal_cord_sc = None
        self.failure_detector_sc = None

    def setup(self):
        self.spinal_cord_sc = rospy.Subscriber('/gopher_spinal_cord/blackboard', String, self.spinal_cord_callback)
        self.failure_detector_sc = rospy.Subscriber('/gopher_failure_detector/blackboard', String,
                                                    self.failure_detector_callback)

    def shutdown(self):
        self.spinal_cord_sc.unregister()
        self.failure_detector_sc.unregister()

    def spinal_cord_callback(self, data):
        """
        /gopher_spinal_cord/blackboard = robot's status
        :param data:
        :return:
        """
        self.blackboard.add_attr('spinal_cord', str(data))

    def failure_detector_callback(self, data):
        """
        /gopher_failure_detector/blackboard = failure status
        :param data:
        :return:
        """
        self.blackboard.add_attr('failure_detector', str(data))

    def pose_callback(self, data):
        """
        /navi/pose = robot's pose
        :param data:
        :return:
        """
        self.blackboard.add_attr('pose_x', data.pose.pose.position.x)
        self.blackboard.add_attr('pose_y', data.pose.pose.position.y)
