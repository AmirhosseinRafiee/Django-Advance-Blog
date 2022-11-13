from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from .models import Post

''' Function based view show a template
def index_view(request):
    """
    a function based view to show index page
    """
    name = 'ali'
    context = {'name': name}
    return render(request, 'index.html', context)
'''
class IndexView(TemplateView):
    '''
    a class based view to show index page
    '''
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'amir'
        context['posts'] = Post.objects.all()
        return context

''' FBV for redirect
from django.shortcuts import redirect
def redirect_to_geeks(request):
    return redirect('https://geeksforgeeks.org')
'''

class RedirectToGeeks(RedirectView):
    '''
    Redirection view sample for maktabkhooneh
    '''
    url = "https://geeksforgeeks.org"

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)
