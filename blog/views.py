from django.template import Context, RequestContext, loader
from blog.models import Post, Category
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, DetailView

def obsolete_post(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    return HttpResponsePermanentRedirect(post.get_absolute_url())

class IndexView(View):
    template_name = "blog/index.html"
    def get(self, request):
        return render(
            request,
            self.template_name, 
            {
                'new_posts' : Post.objects.all().order_by('-date')[0:3],
                'previous_posts' : Post.objects.all().order_by('-date')[3:],
            }                
        )

class PostView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post.html"