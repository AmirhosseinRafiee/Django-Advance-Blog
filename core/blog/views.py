from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from .models import Post
from .forms import PostFrom

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
    """
    a class based view to show index page
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "amir"
        context["posts"] = Post.objects.all()
        return context


""" FBV for redirect
from django.shortcuts import redirect
def redirect_to_geeks(request):
    return redirect('https://geeksforgeeks.org')
"""


class RedirectToGeeks(RedirectView):
    """
    Redirection view sample for maktabkhooneh
    """

    url = "https://geeksforgeeks.org"

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)


class PostListView(ListView):
    # model = Post
    queryset = Post.objects.filter(status=True)
    context_object_name = "posts"
    paginate_by = 2
    ordering = "-published_date"


class PostDetailView(LoginRequiredMixin, DetailView):
    # model = Post
    queryset = Post.objects.filter(status=True)
    context_object_name = "post"


"""
class PostCreateView(FormView):
    template_name = 'post_form.html'
    form_class = PostForm
    success_url = '/blog/post/'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
"""


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "blog.add_post"
    model = Post
    # fields = ('author','title', 'content', 'status', 'category', 'published_date')
    form_class = PostFrom
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "blog.change_post"
    model = Post
    form_class = PostFrom
    success_url = "/blog/post/"


class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = "blog.delete_post"
    model = Post
    success_url = "/blog/post"
