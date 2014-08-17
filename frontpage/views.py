from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView

from articles.models import Article
from blog.models import Post
from events.models import Event
from frontpage.models import CarouselItem
from songs.models import Song


class SiteIndex(TemplateView):
    template_name = "frontpage/index.html"
    SONG_COUNT = 10

    def get_context_data(self, **kwargs):
        context = super(SiteIndex, self).get_context_data(**kwargs)
        context['carousel_items'] = CarouselItem.objects.filter(archived=False)
        context['events'] = Event.current.all()
        context['post'] = Post.objects.all().order_by('-date')[0]
        context['songs'] = Song.objects.all().order_by('-date')[:SiteIndex.SONG_COUNT]
        return context


class About(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        authors = []
        for user in User.objects.filter(is_active=True):
            author = {}
            author['user'] = user
            author['songs'] = Song.po.filter(author=user).count()
            author['articles'] = Article.po.filter(author=user).count()
            author['events'] = Event.po.filter(author=user).count()
            author['total'] = author['songs'] + author['articles'] + author['events']
            if author['total']:
                authors.append(author)
        context['authors'] = sorted(authors, key=lambda k: k['total'], reverse=True)
        return context


class Hello(FormView):
    form_class = AuthenticationForm
    template_name = "hello.html"
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(Hello, self).get_context_data(**kwargs)
        if self.request.GET and 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.GET and 'next' in self.request.GET:
            return HttpResponseRedirect(self.request.GET['next'])
        return super(Hello, self).form_valid(form)


class Goodbye(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))
