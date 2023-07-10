CELERY_BROKER_URL = 'redis://localhost/0'
# CELERY_RESULT_BACKEND = 'redis://172.17.0.2:6379/0'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CELERY_BROKER_TRANSPORT = 'redis'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

CELERY_BEAT_SCHEDULE = {
    # 'get_wallets_balances': {
    #     'task': 'account.tasks.get_wallets_balances',
    #     'schedule': 60,
    # }
}