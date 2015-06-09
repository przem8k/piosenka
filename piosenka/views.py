from datetime import datetime, timedelta
import random
import hashlib

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView, CreateView

from articles.models import Article
from blog.models import Post
from events.models import Event
from frontpage.models import CarouselItem
from songs.models import Annotation, Song
from piosenka.forms import InvitationForm
from piosenka.models import Invitation


class StaffOnlyMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not (self.request.user.is_staff):
            raise Http404
        return super().dispatch(*args, **kwargs)


class SiteIndex(TemplateView):
    template_name = "frontpage/index.html"
    POST_COUNT = 1
    SONG_COUNT = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carousel_items'] = CarouselItem.objects.filter(archived=False)
        context['events'] = (Event.items_visible_to(self.request.user)
                             .filter(datetime__gte=datetime.now())
                             .order_by('datetime'))
        context['posts'] = (Post.items_visible_to(self.request.user)
                            .order_by('-pub_date')[:SiteIndex.POST_COUNT])
        context['songs'] = (Song.items_visible_to(self.request.user)
                            .order_by('-pub_date')[:SiteIndex.SONG_COUNT])
        context['annotation'] = (Annotation.items_visible_to(self.request.user)
                                 .order_by('-pub_date').first())
        return context


class About(TemplateView):
    ARTICLE_FACTOR = 5
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        authors = []
        for user in User.objects.filter(is_active=True):
            author = {}
            author['user'] = user
            author['annotations'] = Annotation.live.filter(author=user).count()
            author['songs'] = Song.live.filter(author=user).count()
            author['articles'] = Article.live.filter(author=user).count()
            author['events'] = Event.live.filter(author=user).count()
            author['total'] = (author['annotations'] + author['songs'] +
                               self.ARTICLE_FACTOR * author['articles'] +
                               author['events'])
            if author['total']:
                authors.append(author)
        context['authors'] = sorted(authors, key=lambda k: k['total'],
                                    reverse=True)
        return context


class Format(TemplateView):
    template_name = "format.generated"


class Hello(FormView):
    form_class = AuthenticationForm
    template_name = "hello.html"
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET and 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.GET and 'next' in self.request.GET:
            return HttpResponseRedirect(self.request.GET['next'])
        return super().form_valid(form)


class Goodbye(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))


class ChangePassword(FormView):
    form_class = PasswordChangeForm
    template_name = "change_password.html"
    success_url = reverse_lazy('index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ToReview(StaffOnlyMixin, TemplateView):
    template_name = "to_review.html"


class InviteView(StaffOnlyMixin, CreateView):
    model = Invitation
    form_class = InvitationForm
    template_name = "invite.html"

    def form_valid(self, form):
        text_to_hash = str(random.random()) + form.instance.email_address
        h = hashlib.sha256(text_to_hash.encode('utf-8'))
        form.instance.invitation_key = h.hexdigest()
        form.instance.expires_on = datetime.today() + timedelta(7)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')
