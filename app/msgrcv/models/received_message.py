from lxml import objectify
from text_message_content import TextMessageContent
import logging
import config

logging = logging.getLogger("received_message")

class ReceivedMessage(object):
    create_time = ''
    to_user_name = ''
    from_user_name = ''
    msg_type = ''
    msg_id = ''
    msg_content = None

    def __init__(self):
        pass

    def __del__(self):
        pass

    def buildFromXml(self, data):
        #create_time, to_user_name, from_user_name, msg_id, media_id, msg_type, content, pic_url = None
        try:
            msg_root = objectify.fromstring(data)
        except:
            logging.warning("parser_xml_object_error")
            return False
        if msg_root.find('ToUserName') is not None and len(msg_root.ToUserName.text) > 0:
            self.to_user_name = msg_root.ToUserName.text
        else:
            logging.warning("to_user_name_empty")
            return False

        if msg_root.find('FromUserName') is not None and len(msg_root.FromUserName.text) > 0:
            self.from_user_name = msg_root.FromUserName.text
        else:
            logging.warning("from_user_name_empty")
            return False

        if msg_root.find('MsgId') is not None and len(msg_root.MsgId) > 0:
            self.msg_id = msg_root.MsgId.text
        else:
            logging.warning("message_id_empty")
            return False

        if msg_root.find('CreateTime') is not None and len(msg_root.CreateTime.text) > 0:
            self.create_time = msg_root.CreateTime.text
        else:
            logging.warning("create_time_empty")
            return False

        if msg_root.find('MsgType') is not None and len(msg_root.MsgType.text) > 0 \
                and msg_root.MsgType.text in config.MSG_TYPES:
            self.msg_type = msg_root.MsgType.text
        else:
            logging.warning("message_type_error")
            return False

        if self.msg_type == config.MSG_TYPE_TEXT:
            self.msg_content = TextMessageContent()
            self.msg_content.buildFromXmlRoot(msg_root)

        return True
