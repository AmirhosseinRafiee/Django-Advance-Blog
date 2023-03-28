from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
import requests
from .tasks import send_email_task


def send_email(request):
    send_email_task.delay()
    return HttpResponse("<h1>Done Sending</h1>")

def test_view(request):
    if cache.get("test_delay_api") is None:
        response = requests.get("https://07b35e6e-6cbd-41d5-9093-a84d0b388049.mock.pstmn.io/test/delay/5")
        cache.set("test_delay_api", response.json(), 2)
    return JsonResponse(cache.get("test_delay_api"))
