from blog.models import Post
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
