from django_cron import CronJobBase, Schedule
from portfolio_test.views import populate_stock_history


class MyCronJob(CronJobBase):

    RUN_AT_TIMES = ['2:00']

    print("inside cron")

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    code = 'portfolio_prophet.cron.MyCronJob'    # a unique code

    populate_stock_history('')
        