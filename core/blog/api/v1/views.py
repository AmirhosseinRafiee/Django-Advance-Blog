from rest_framework.decorators import api_view
from rest_framework.response import Response

data = {
    'title': 'hello'
}

@api_view()
def post_list(request):
    return Response('ok')

@api_view()
def post_detail(request, id):
    data['id'] = id
    return Response(data)
