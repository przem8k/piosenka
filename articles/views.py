from django.views.generic import DetailView, TemplateView

from articles.models import Article

class ArticleView(DetailView):
    model = Article
    context_object_name = "article"
    template_name = "articles/article.html"

class IndexView(TemplateView):
    FEATURED_COUNT = 3

    template_name = "articles/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['featured'] = Article.objects.all()[0:self.FEATURED_COUNT]
        return context

