from celery import shared_task
from time import sleep


@shared_task
def send_email_task():
    sleep(4)
    print("done sending email")
