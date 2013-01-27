from blog.models import Post
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, DetailView


def obsolete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return HttpResponsePermanentRedirect(post.get_absolute_url())


class IndexView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['new_posts'] = Post.objects.all().order_by('-date')[0:5]
        context['all_posts'] = Post.objects.all().order_by('-date')
        return context


class PostView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post.html"

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all().order_by('-date')
        return context
