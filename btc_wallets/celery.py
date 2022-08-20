import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btc_wallets.settings')

app = Celery('btc_wallets')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'get_rate_every_half_an_hour': {
        'task': 'api.tasks.rate',
        'schedule': 30*60.0,
    }
}
