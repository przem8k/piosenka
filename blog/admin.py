from blog.models import Post, Category
from django.contrib import admin
from datetime import datetime

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug' : ['title'] }
	fields = ('title', 'slug', 'category', 'post', 'more', )
	def save_model(self, request, obj, form, change):
		if not change:
			obj.author = request.user
			obj.date = datetime.today()
		obj.save()

admin.site.register(Post, PostAdmin)
admin.site.register(Category)

