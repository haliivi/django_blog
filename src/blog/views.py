from django.contrib.auth import login, authenticate
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from django.conf import settings
from taggit.models import Tag
from .models import *
from .forms import *

__all__ = [
    'IndexView',
    'PostDetailView',
    'SignUpView',
    'SignInView',
    'FeedBackView',
    'SuccessView',
    'SearchResultsView',
    'TagView',
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
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:5]
        context['post'] = post
        context['common_tags'] = common_tags
        context['last_posts'] = last_posts
        return context

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            post = get_object_or_404(Post, url=slug)
            Comment.objects.create(post=post, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'blog/post_detail.html', context={
            'comment_form': comment_form
        })


class SignUpView(FormView):
    template_name = 'blog/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class SignInView(FormView):
    template_name = 'blog/signin.html'
    form_class = SignInForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)


class FeedBackView(FormView):
    template_name = 'blog/contacts.html'
    form_class = FeedBackForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        from_email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        try:
            send_mail(f'От {name} | {subject}', message, from_email, [settings.EMAIL_HOST_USER])

        except BadHeaderError:
            return HttpResponse('Невалидный заголовок')
        return HttpResponseRedirect('success')


class SuccessView(TemplateView):
    template_name = 'blog/success.html'


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ''
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/search.html', context={
            'page_obj': page_obj,
            'count': paginator.count
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'blog/tag.html', context={
            'title': f'#ТЕГ {tag}',
            'posts': posts,
            'common_tags': common_tags
        })
