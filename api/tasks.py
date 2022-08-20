import requests

from celery import shared_task
from django.core.cache import cache
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from btc_wallets.settings import EXCHANGE_API_APP_ID, EXCHANGE_API_URL, FAKE_RATE


logger = get_task_logger(__name__)


@shared_task
def rate():
    params = {'app_id': EXCHANGE_API_APP_ID}
    try:
        response = requests.get(EXCHANGE_API_URL, params=params)
        result = response.json().get('rates').get('BTC')
        logger.info("Rate value has been set")
    except Exception:
        result = FAKE_RATE
        logger.info("Fake rate value has been set")
    cache.set("rate", result)
    return result


@worker_ready.connect
def at_start(sender, **kwargs):
    """Run tasks at startup"""
    with sender.app.connection() as conn:
        sender.app.send_task("api.tasks.rate", connection=conn)
