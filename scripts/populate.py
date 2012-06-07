from blog.models import Post
from django.contrib.auth.models import User
from datetime import datetime

me = User.objects.get(id=1)
first_post = Post()
first_post.author = me
first_post.date = datetime.now()
first_post.title = 'My first post!'
first_post.post = 'How exciting. That is all!'
first_post.save()
