import os
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=9, minute=30)
def scheduled_investment():
    print("Starting scheduled investment...")
    subprocess.run(["python", "main.py"])
    print("Investment job completed")

# For testing - run immediately on deploy
if os.environ.get('RUN_ON_DEPLOY', 'false').lower() == 'true':
    scheduled_investment()

sched.start()