from django import forms

from articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('published', 'slug', 'lead_text', 'main_text', 'cover_credits')
