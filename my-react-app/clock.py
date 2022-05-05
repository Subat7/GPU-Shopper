from apscheduler.schedulers.blocking import BlockingScheduler
from main import *

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=20)
def timed_job():
    main_call_frame()
    #print("Running scheduled job")

sched.start()