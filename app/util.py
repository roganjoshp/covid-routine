import re


WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 
            'Sunday']


day_dict = {0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday', 
            5: 'Saturday',
            6: 'Sunday'}


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def handle_ajax_error(msg_dict):
    
    if msg_dict['status']:
        msg_dict['message'] = '<font style="color: green">{}</font>'.format(
                                                             msg_dict['message']
                                                             )
    else:
        msg_dict['message'] = '<font style="color: red">{}</font>'.format(
                                                             msg_dict['message']
                                                             )
    return msg_dict