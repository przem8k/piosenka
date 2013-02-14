from django.views.generic import DetailView, TemplateView

from articles.models import Article

class ArticleView(DetailView):
    model = Article
    context_object_name = "article"
    template_name = "articles/article.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['model_meta'] = Article._meta
        return context

class IndexView(TemplateView):
    template_name = "articles/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context

