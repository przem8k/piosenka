from django.contrib import admin

from articles.models import Article, ArticleCategory

class ArticleAdmin(admin.ModelAdmin):
    pass

class ArticleCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
