from ..blackboard import BlackBoard


class StatusDetector(object):

    def __init__(self):
        self.blackboard = BlackBoard.get_instance()
        self.last_status = ""
        self.policy = {}

    def setup(self):
        self.policy = self.blackboard.get_attr()['policy_config']

    def detect(self):
        current_status = self.blackboard.status
        if current_status in self.policy and current_status != self.last_status:
            print('{} is detected!'.format(current_status))
            log_policy = self.policy[current_status]['log']
            message_policy = self.policy[current_status]['message']
            report = {
                'detector': StatusDetector.__name__,
                'topic': current_status,
                'detect': True,
                'message': message_policy,
                'log': log_policy,
            }
        else:
            report = {
                'detector': StatusDetector.__name__,
                'detect': False
            }
        self.last_status = current_status
        return report
