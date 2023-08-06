#!/usr/bin/env python

import rospy

from problem_detector.problem_detector import ProblemDetector

if __name__ == '__main__':
    rospy.init_node('problem_detector')
    print("Problem Detector is started!")
    problem_detector = ProblemDetector()
    problem_detector.main()
    rospy.on_shutdown(problem_detector.shutdown)
    rospy.spin()
