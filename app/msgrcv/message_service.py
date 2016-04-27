__author__ = 'linfengji'

from models.wc_message import WcMessage
from lxml import etree
import redis
import logging

logging = logging.getLogger("wc_message")


def getTextFromRedis(from_user_name):
    key = "message_text_" + from_user_name
    try:
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        result_text = r.get(key)
        if not result_text:
            result_text = "empty_content"
        logging.info("get_text_op;key=%s;get_text=%s" %(key, result_text))
    except:
        result_text = "get_text_error"
    return result_text

def setTextToRedis(from_user_name, text):
    key = "message_text_" + from_user_name
    try:
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        result_text = r.set(key, text)
        logging.info("set_text_op;key=%s;set_text=%s" %(key, result_text))
    except:
        return "set_text_error"
    return "set_text_ok"

def processTextMessage(rcv_msg): 
    snd_msg_root = etree.Element("xml")
    if rcv_msg.msg_content and rcv_msg.msg_content.msg_content:
        tokens = rcv_msg.msg_content.msg_content.strip().split(" ")
        if tokens[0] == 'get':
            result_text = getTextFromRedis(rcv_msg.from_user_name)
            etree.SubElement(snd_msg_root, "Content").text = result_text.decode('utf-8')
        elif tokens[0] == 'set':
            msg_content = ' '.join(tokens[1:])
            result_text = setTextToRedis(rcv_msg.from_user_name, msg_content)
            etree.SubElement(snd_msg_root, "Content").text = result_text.decode('utf-8')
        else: 
            etree.SubElement(snd_msg_root, "Content").text = "wrong_command"
    else:
        etree.SubElement(snd_msg_root, "Content").text = rcv_msg.msg_content.msg_content
    etree.SubElement(snd_msg_root, "ToUserName").text = rcv_msg.from_user_name
    etree.SubElement(snd_msg_root, "FromUserName").text = rcv_msg.to_user_name
    etree.SubElement(snd_msg_root, "CreateTime").text = rcv_msg.create_time
    etree.SubElement(snd_msg_root, "MsgType").text = rcv_msg.msg_type
    return etree.tostring(snd_msg_root, encoding="UTF-8", pretty_print=False)


def setUserMessage(usr_msg):
    try:
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.set('message_text_' + usr_msg.username, usr_msg.text)
    except:
        return False
    return True
