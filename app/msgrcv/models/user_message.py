__author__ = 'linfengji'

import logging

logging = logging.getLogger("user_message")

class UserMessage(object):
    username = ''
    text = ''

    def __init__(self):
        pass

    def __del__(self):
        pass

    def buildFromUrlParameter(self, request_args):
        try:
            self.username = request_args.get("username")
            self.text = request_args.get("text")
        except:
            logging.warning("error_content_parameter")
        if self.username and len(self.username) > 0 :
            return True
        else:
            return False
