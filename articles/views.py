from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView

from articles.forms import ArticleForm
from articles.models import Article
from piosenka.trevor import put_text_in_trevor
from piosenka.mixins import ContentItemEditMixin, ContentItemAddMixin
from piosenka.mixins import ContentItemViewMixin
from piosenka.mixins import ContentItemApproveMixin


class IndexView(TemplateView):
    template_name = "articles/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.items_visible_to(self.request.user).all()
        return context


class ArticleView(ContentItemViewMixin, DetailView):
    model = Article
    context_object_name = "article"
    template_name = "articles/article.html"


class AddArticle(ContentItemAddMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/add_edit_article.html"

    def get_initial(self):
        initial_lead = "Tu wpisz **lead** artykułu - " \
                       "jedno lub dwa zdania otwierające tekst."
        initial_main = "Tu wpisz resztę artykułu."
        return {
            'lead_text_trevor': put_text_in_trevor(initial_lead),
            'main_text_trevor': put_text_in_trevor(initial_main),
        }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditArticle(ContentItemEditMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/add_edit_article.html"

    def get_object(self):
        return get_object_or_404(Article, slug=self.kwargs['slug'])

    def get_success_url(self):
        return self.object.get_absolute_url()


class ApproveArticle(ContentItemApproveMixin, RedirectView):
    def get_object(self):
        return get_object_or_404(Article, slug=self.kwargs['slug'])
