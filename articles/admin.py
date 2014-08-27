from django.contrib import admin

from articles.models import Article

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Article, ArticleAdmin)
