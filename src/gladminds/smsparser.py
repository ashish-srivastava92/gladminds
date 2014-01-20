from parse import *
from gladminds import utils, message_template as templates

class InvalidMessage(Exception):{}

def sms_parser(*args, **kwargs):
    message = kwargs['message']
    parse_message = parse(templates.RCV_MESSAGE_FORMAT, message)
    keyword = parse_message['key']
    if not parse_message:
        raise InvalidMessage("incorrect message format")
        
    #Check appropriate received message template and parse the message data
    template_mapper = templates.RCV_MESSAGE_TEMPLATE_MAPPER
    if keyword.lower() in template_mapper.keys():
        key_args = parse(template_mapper[keyword], parse_message['message'])
        if not key_args:
            raise InvalidMessage("invalid message")
        return key_args.named
    else:
        raise InvalidMessage("invalid message")

def sms_formater(*args, **kwargs):
    pass
    
    
    