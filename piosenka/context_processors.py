from django.conf import settings

from songs.models import ArtistNote, Song, SongNote


def to_review(request):
    to_review = []
    to_review.extend(ArtistNote.items_reviewable_by(request.user))
    to_review.extend(Song.items_reviewable_by(request.user))
    to_review.extend(SongNote.items_reviewable_by(request.user))
    return {"to_review": to_review}
