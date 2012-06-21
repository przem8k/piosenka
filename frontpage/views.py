from django.views.generic import View
from django.shortcuts import render

from blog.models import Post
from events.models import Event


class IndexView(View):
    template_name = "frontpage/index.html"
    post_count = 5

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                'posts': Post.objects.all().order_by('-date')[0:IndexView.post_count],
                'events': Event.current.all(),
            }
        )
