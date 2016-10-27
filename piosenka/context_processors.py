from articles.models import Article
from blog.models import Post
from events.models import Event
from songs.models import ArtistNote, SongNote, Song


def to_review(request):
    to_review = []
    to_review.extend(Article.items_reviewable_by(request.user))
    to_review.extend(ArtistNote.items_reviewable_by(request.user))
    to_review.extend(Event.items_reviewable_by(request.user))
    to_review.extend(Post.items_reviewable_by(request.user))
    to_review.extend(Song.items_reviewable_by(request.user))
    to_review.extend(SongNote.items_reviewable_by(request.user))
    return {'to_review': to_review}
