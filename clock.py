import os
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day=24, hour=11, minute=28)
def scheduled_investment():
    print("Starting monthly investment...")
    subprocess.run(["python", "main.py"])
    print("Monthly investment job completed")

# For testing - run immediately on deploy
if os.environ.get('RUN_ON_DEPLOY', 'false').lower() == 'true':
    scheduled_investment()

sched.start()