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
    template_mapper = templates.MESSAGE_TEMPLATE_MAPPER
    lower_keyword = keyword.lower()
    if lower_keyword in template_mapper.keys():
        key_args = parse(template_mapper[lower_keyword]['receive'], parse_message['message'])
        if not key_args:
            raise InvalidMessage("invalid message")
        #Added the Message keyword and handler in return dictionary
        key_args.named['keyword'] = lower_keyword
        key_args.named['handler'] = template_mapper[lower_keyword]['handler']
        key_args.named['auth_rule'] = template_mapper[lower_keyword]['auth_rule']
        return key_args.named
    else:
        raise InvalidMessage("invalid message")

def render_sms_template(*args, **kwargs):
    key = kwargs.get('key', None)
    template = kwargs.get('template', None)
    message = None
    if template:
        message = template.format(*args, **kwargs)
    
    if not template and key:
        status = kwargs.get('status', None)
        template_mapper = templates.MESSAGE_TEMPLATE_MAPPER[key]
        message_template = template_mapper[status]
        message = message_template.format(*args, **kwargs)
    return message