from django.shortcuts import HttpResponse
from .tasks import send_email_task


def send_email(request):
    send_email_task.delay()
    return HttpResponse("<h1>Done Sending</h1>")
