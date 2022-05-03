from apscheduler.schedulers.blocking import BlockingScheduler
from main import *

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=60)
def timed_job():
    main_call_frame()
    #print("Running scheduled job")

sched.start()