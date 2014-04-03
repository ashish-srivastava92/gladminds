import logging
logger = logging.getLogger('gladminds')
from parse import *
from gladminds import utils, message_template as templates

class SmsException(Exception):
    def __init__(self, message=None, template = None):
        Exception.__init__(self, message)
        self.template = template
        
class InvalidMessage(SmsException):{}

class InvalidKeyWord(SmsException):{}

class InvalidFormat(SmsException): {}

def sms_parser(*args, **kwargs):
    message = kwargs['message']

    parse_message = parse(templates.RCV_MESSAGE_FORMAT, message)

    keyword = None
    try:
        keyword = parse_message['key']
    except:
        raise InvalidMessage(message = 'invalid message', template = templates.get_template('SEND_INVALID_MESSAGE'))
    if not parse_message:
        raise InvalidMessage(message = 'invalid message', template = templates.get_template('SEND_INVALID_MESSAGE'))
    #Check appropriate received message template and parse the message data
    template_mapper = templates.get_message_template_mapper()
    lower_keyword = keyword.lower()
    if lower_keyword in template_mapper.keys():
        key_args = parse(template_mapper[lower_keyword]['receive'], parse_message['message'])
        logging.info("valid message format")
        if not key_args:
            raise InvalidFormat(message = 'invalid message format', template = keyword+' '+template_mapper[lower_keyword]['receive'])
        #Added the Message keyword and handler in return dictionary
        key_args.named['keyword'] = lower_keyword
        key_args.named['handler'] = template_mapper[lower_keyword]['handler']
        key_args.named['auth_rule'] = template_mapper[lower_keyword]['auth_rule']
        return key_args.named
    else:
        raise InvalidKeyWord(message = 'invalid keyword' , template = templates.get_template('SEND_CUSTOMER_SUPPORTED_KEYWORD'))


def render_sms_template(keyword=None, status = None, template = None, *args, **kwargs):
    keyword = keyword
    template = template
    message = None
    if template:
        message = template.format(*args, **kwargs)
    
    if not template and keyword:
        status = status
        template_mapper = templates.get_message_template_mapper()
        template_obj = template_mapper[keyword]
        message_template = template_obj[status]
        message = message_template.format(*args, **kwargs)
    return message