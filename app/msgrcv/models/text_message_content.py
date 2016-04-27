import logging

logging = logging.getLogger("text_message_content")


class TextMessageContent(object):
    msg_content = ''

    def __init__(self):
        pass

    def __del__(self):
        pass

    def buildFromXmlRoot(self, xmlRoot):
        if xmlRoot.find('Content') is not None and len(xmlRoot.Content.text) > 0:
            self.msg_content = xmlRoot.Content.text
        else:
            logging.warning("Content_empty")
            return False
        return True;