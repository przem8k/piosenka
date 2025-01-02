from django.conf import settings

from articles.models import Article
from blog.models import Post
from songs.models import ArtistNote, Song, SongNote


def to_review(request):
    to_review = []
    to_review.extend(Article.items_reviewable_by(request.user))
    to_review.extend(ArtistNote.items_reviewable_by(request.user))
    to_review.extend(Post.items_reviewable_by(request.user))
    to_review.extend(Song.items_reviewable_by(request.user))
    to_review.extend(SongNote.items_reviewable_by(request.user))
    return {"to_review": to_review}
