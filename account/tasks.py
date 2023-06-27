from celery import shared_task


@shared_task
def generate_random_number():
    print("task run!!")
