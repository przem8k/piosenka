from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from articles.forms import ArticleForm
from articles.models import Article
from content.trevor import put_text_in_trevor
from content.mixins import ContentItemEditMixin, ContentItemAddMixin
from content.views import ReviewContentView
from content.views import ApproveContentView
from content.views import ViewContentView


class GetArticleMixin(object):
    def get_object(self):
        return get_object_or_404(Article, slug=self.kwargs['slug'])


class IndexView(TemplateView):
    template_name = "articles/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.items_visible_to(self.request.user).all()
        return context


class ViewArticle(GetArticleMixin, ViewContentView):
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


class EditArticle(GetArticleMixin, ContentItemEditMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/add_edit_article.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReviewArticle(GetArticleMixin, ReviewContentView):
    pass


class ApproveArticle(GetArticleMixin, ApproveContentView):
    pass
