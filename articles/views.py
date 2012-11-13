from django.views.generic import DetailView

from articles.models import Article

class ArticleView(DetailView):
    model = Article
    context_object_name = "post"
    template_name = "articles/article.html"
