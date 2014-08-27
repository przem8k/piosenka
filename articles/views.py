from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from articles.forms import ArticleForm
from articles.models import Article
from frontpage.views import CheckAuthorshipMixin, CheckLoginMixin


class IndexView(TemplateView):
    template_name = "articles/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(DetailView):
    model = Article
    context_object_name = "article"
    template_name = "articles/article.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['can_edit'] = self.request.user.is_active and (
            self.request.user.is_staff or self.request.user == self.object.author)
        return context


class AddArticle(CheckLoginMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/add_edit_article.html"
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddArticle, self).form_valid(form)


class EditArticle(CheckAuthorshipMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/add_edit_article.html"

    def get_object(self):
        return get_object_or_404(Article, slug=self.kwargs['slug'])

    def get_success_url(self):
        return self.object.get_absolute_url()
