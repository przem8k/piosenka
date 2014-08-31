from django.contrib import admin

from articles.models import Article

class ArticleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Article, ArticleAdmin)
