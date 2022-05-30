# -*- coding: utf-8 -*-
"""
Created on Mon May 30 10:26:24 2022

@author: garym
"""

import schedule

from datetime import datetime, time

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

# Original test case from OP
if is_time_between(time(8,30), time(19,30)):
        print("I'm working...")


def job():
    print("I'm working...")


now = datetime.utcnow().time()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#schedule.every(10).seconds.do(job)

#while True:
#    schedule.run_pending()
#    time.sleep(1)