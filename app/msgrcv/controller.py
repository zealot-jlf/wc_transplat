from flask import Blueprint, request, render_template
from hashlib import sha1
from models.wc_message import WcMessage
from models.user_message import UserMessage
import message_service
import logging
import config

mod_msgrcv = Blueprint('rcv', __name__, url_prefix='/wc')
logging = logging.getLogger("msgrcv")


def check_sign():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echo_str = request.args.get('echostr')
    if signature is None or len(signature) == 0 \
            or timestamp is None or len(timestamp) == 0 \
            or nonce is None or len(nonce) == 0\
            or echo_str is None or len(echo_str) == 0:
        return "invalid_request;wrong_parameter"

    csign = sha1(''.join(sorted([config.TOKEN, timestamp, nonce]))).hexdigest()
    logging.info("get_sign_message;calulated_signature:%s;raw_signature", csign, signature)

    if signature == csign:
        return echo_str
    else:
        return "invalid_request;wrong_signature"


def handler_msg():
    rcv_msg = WcMessage()
    if rcv_msg.buildFromXml(request.data):
        logging.info("rcv_msg;from_user=%s;to_user=%s" %(rcv_msg.from_user_name, rcv_msg.to_user_name))
        return message_service.processTextMessage(rcv_msg)
    else:
        return "invalid_message_format"


@mod_msgrcv.route('/', methods=['GET', 'POST'])
def message_receive():
    # validateServer
    logging.info("get_wc_msg\t%s" %(request.get_data()))
    if request.method == 'GET':
        return check_sign()
    elif request.method == 'POST':
        ret_msg =  handler_msg()
        logging.info("ret_msg=%s" %(ret_msg))
        return ret_msg
    else:
        return "invalid_wechat_request"

@mod_msgrcv.route('/set_msg', methods=['GET', 'POST'])
def message_set():
    #message set to cache
    logging.info("get_user_msg_to_set\t%s" %(request.get_data()))
    usr_msg = UserMessage()
    if usr_msg.buildFromUrlParameter(request.args):
        if message_service.setUserMessage(usr_msg):
            return "set_message_done"
        else:
            return "set_message_fail"
    else:
        return "invalid_set_message_format"
