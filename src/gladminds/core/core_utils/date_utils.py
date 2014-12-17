'''
This file contains all utils related to date
'''
from datetime import datetime
import pytz
from gladminds.settings import TIMEZONE
from gladminds.core.constants import DATE_FORMAT


def get_current_date():
    '''
    Returns current date
    '''
    return datetime.now()


def convert_utc_to_local_time(date, to_string=False):
    utc = pytz.utc
    timezone = pytz.timezone(TIMEZONE)
    if to_string:
        return date.astimezone(timezone).replace(tzinfo=None).strftime(DATE_FORMAT)
    else:
        return date.astimezone(timezone).replace(tzinfo=None)
    
def total_time_spent(feedback_obj):
    wait_time = feedback_obj.wait_time
    if feedback_obj.resolved_date:
        start_date = convert_utc_to_local_time(feedback_obj.created_date)
        end_date = feedback_obj.resolved_date
        start_date, end_date = get_start_and_end_date(start_date,
                                                     end_date, TIME_FORMAT)
        wait = end_date - start_date
        wait_time = wait.total_seconds() 
        wait_time = wait_time - feedback_obj.wait_time
        minutes, seconds = divmod(wait_time, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        weeks, days = divmod(days, 7)
        return " {0} days ,{1}:{2}:{3}" .format(int(days),int(hours),int(minutes),int(seconds))

def get_start_and_end_date(start_date, end_date, format):

    start_date = start_date.strftime(format)
    start_date = datetime.datetime.strptime(start_date, format)
    end_date = end_date.strftime(format)
    end_date = datetime.datetime.strptime(end_date, format)
    return start_date,end_date

def gernate_years():
    start_year = 2013
    current_year = datetime.date.today().year
    year_list = []
    for date in range(start_year, current_year+1):
        year_list.append(date)
    return year_list


def get_time_in_seconds(time, unit):
    if unit == 'days':
        total_seconds = time * 86400
    elif unit == 'hrs':
        total_seconds = time * 3600
    else:
        total_seconds = time * 60
    return total_seconds