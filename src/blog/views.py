from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import *

__all__ = [
    'IndexView',
    'PostDetailView',
]


class IndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class PostDetailView(TemplateView):
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        post = get_object_or_404(Post, url=slug)
        context['post'] = post
        return context
