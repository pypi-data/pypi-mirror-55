import requests
import json
import os
import yaml


class Client(object):
    def __init__(self):
        pkg_path = os.path.dirname(__file__)
        config_file_path = os.path.join(pkg_path, 'config/server_config.yaml')
        with open(config_file_path, 'r') as config_file:
            config = yaml.load(config_file, yaml.BaseLoader)
            self.slack_proxy_server_ip = config['slack_proxy_server_ip']
            self.slack_proxy_server_port = config['slack_proxy_server_port']

    def post_message(self, message):
        route = 'post-message'
        url = "http://{}:{}/{}".format(self.slack_proxy_server_ip, self.slack_proxy_server_port, route)
        request_text = {
            "text": message,
        }
        response = requests.post(url, data=json.dumps(request_text))
        return response.status_code

    def post_file(self, file):
        route = 'post-file'
        url = "http://{}:{}/{}".format(self.slack_proxy_server_ip, self.slack_proxy_server_port, route)

        request_data = dict()
        request_file = dict()

        request_file['upload_file'] = file
        response = requests.post(url, data=request_data, files=request_file)
        return response.status_code
