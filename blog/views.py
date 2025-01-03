import time
from datetime import datetime

from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from blog.forms import PostForm
from blog.models import Post
from content.views import (AddContentView, ApproveContentView, EditContentView,
                           ReviewContentView, ViewContentView)


class GetPostMixin:
    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs["slug"])


def obsolete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return HttpResponsePermanentRedirect(post.get_absolute_url())


class PostIndex(TemplateView):
    MAX_POSTS = 5
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_posts"] = Post.items_visible_to(self.request.user)[
            0 : PostIndex.MAX_POSTS
        ]
        context["all_posts"] = Post.items_visible_to(self.request.user)
        return context


class ViewPost(GetPostMixin, ViewContentView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_posts"] = Post.items_visible_to(self.request.user)
        return context


class AddPost(AddContentView):
    model = Post
    form_class = PostForm
    template_name = "blog/add_edit_post.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditPost(GetPostMixin, EditContentView):
    model = Post
    form_class = PostForm
    template_name = "blog/add_edit_post.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReviewPost(GetPostMixin, ReviewContentView):
    pass


class ApprovePost(GetPostMixin, ApproveContentView):
    pass
