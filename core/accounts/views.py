from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
# from django.core.cache import cache
import requests
from .tasks import send_email_task


def send_email(request):
    send_email_task.delay()
    return HttpResponse("<h1>Done Sending</h1>")


@cache_page(60)
def test_view(request):
    response = requests.get(
        "https://07b35e6e-6cbd-41d5-9093-a84d0b388049.mock.pstmn.io/test/delay/5"
    )
    return JsonResponse(response.json())
