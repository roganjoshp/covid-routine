import re


WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 
            'Sunday']

def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]


def parse_shift_time(day, timestamp):
    day_comp = day * 1440
    hour, minute = timestamp.split(':')
    hour_comp = int(hour) * 60
    minute_comp = int(minute)
    return day_comp + hour_comp + minute_comp


def shift_timestamp_to_human(timestamp):
    day_number = timestamp // 1440
    day = WEEKDAYS[day_number]
    remaining = timestamp - (day_number * 1440)
    hours = int(remaining / 60)
    minutes = remaining - (hours * 60)
    return {'day': day,
            'time': str(hours).zfill(2) + ':' + str(minutes).zfill(2)}