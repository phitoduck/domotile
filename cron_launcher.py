#!/anaconda3/bin/python3

import cron_pipeline

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=10)
def run_pipeline():
    cron_pipeline.run_pipeline(working_dir='~/repos/extra/insidesales')
#     cron_pipeline.run_pipeline(working_dir='.')
    
scheduler.start()