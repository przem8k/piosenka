"""Freezes the db entities as static pages."""

import datetime
import os
import json

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from easy_thumbnails.files import get_thumbnailer
from unidecode import unidecode

from content.trevor import trevor_to_md
from songs.models import Artist, ArtistNote, Song, SongNote

PAGES = ["o-stronie"]

CONTENT_DIR = "pages"

ROOT_PATH = os.path.abspath(os.path.join(__file__, "../../../.."))

BLOG_DIR_PATH = os.path.join(ROOT_PATH, "pages", "blog")

ARTISTS_DIR_PATH = os.path.join(ROOT_PATH, "pages", "spiewnik")

SONGS_DIR_PATH = os.path.join(ROOT_PATH, "pages", "opracowanie")

PZT_MEDIA_URL = "https://storage.googleapis.com/piosenka-media/media/"

def escape(text):
    if not text:
        return None
    # YAML escaping of single quotes
    return text.replace("'", "''")


def create_file_content(item, content):
    frontmatter_lines = ["---"]
    if item.title:
        frontmatter_lines.append(f"title: '{escape(item.title)}'")
    if item.author:
        frontmatter_lines.append(f"author: '{item.author}'")
    if item.pub_date:
        frontmatter_lines.append(f"pub_date: '{item.pub_date}'")
    if hasattr(item, "disambig") and item.disambig:
        frontmatter_lines.append(f"disambig: '{escape(item.disambig)}'")
    if hasattr(item, "original_title") and item.original_title:
        frontmatter_lines.append(f"original_title: '{escape(item.original_title)}'")
    if hasattr(item, "epigone") and item.epigone:
        frontmatter_lines.append(f"epigone: {item.epigone}")
    if hasattr(item, "link_youtube") and item.link_youtube:
        frontmatter_lines.append(f"youtube_id: '{escape(item.youtube_id())}'")
    if hasattr(item, "capo_fret") and item.capo_fret:
        frontmatter_lines.append(f"capo_fret: {item.capo_fret}")

    if hasattr(item, "url1") and item.url1:
        frontmatter_lines.append(f"url1: '{escape(item.url1)}'")
    if hasattr(item, "url2") and item.url2:
        frontmatter_lines.append(f"url2: '{escape(item.url2)}'")
    if hasattr(item, "ref1") and item.ref1:
        frontmatter_lines.append(f"ref1: '{escape(item.ref1)}'")
    if hasattr(item, "ref2") and item.ref2:
        frontmatter_lines.append(f"ref2: '{escape(item.ref2)}'")

    if hasattr(item, "text_authors"):
        artists = item.text_authors()
        if artists:
            frontmatter_lines.append(f"text_authors:")
            for artist in artists:
                frontmatter_lines.append(f" - '{artist.slug}'")
    if hasattr(item, "composers"):
        artists = item.composers()
        if artists:
            frontmatter_lines.append(f"composers:")
            for artist in artists:
                frontmatter_lines.append(f" - '{artist.slug}'")
    if hasattr(item, "translators"):
        artists = item.translators()
        if artists:
            frontmatter_lines.append(f"translators:")
            for artist in artists:
                frontmatter_lines.append(f" - '{artist.slug}'")
    if hasattr(item, "performers"):
        artists = item.performers()
        if artists:
            frontmatter_lines.append(f"performers:")
            for artist in artists:
                frontmatter_lines.append(f" - '{artist.slug}'")

    for score_name in ["score1", "score2", "score3"]:
        if not hasattr(item, score_name):
            continue

        score_field = getattr(item, score_name)
        if not score_field:
            continue

        frontmatter_lines.append(f"{score_name}: {score_field.name}")

        full_url = PZT_MEDIA_URL + score_field.name
        frontmatter_lines.append(f"{score_name}_full: {full_url}")

        thumbnailer = get_thumbnailer(score_field)
        thumbnail = thumbnailer["scorethumb"]
        frontmatter_lines.append(f"{score_name}_thumb: {thumbnail.url}")

    if hasattr(item, "cover_image") and item.cover_image:
        frontmatter_lines.append(f"cover_image: {item.cover_image.name}")
        full_url = PZT_MEDIA_URL + item.cover_image.name
        frontmatter_lines.append(f"cover_image_full: {full_url}")

        thumbnailer = get_thumbnailer(item.cover_image)
        thumbnail_cover = thumbnailer["cover"]
        frontmatter_lines.append(f"cover_image_thumb_600_300: {thumbnail_cover.url}")

        thumbnail_mini = thumbnailer["coverthumb"]
        frontmatter_lines.append(f"cover_image_thumb_420_210: {thumbnail_mini.url}")
        if hasattr(item, "cover_credits_trevor") and item.cover_credits_trevor:
            credits = trevor_to_md(item.cover_credits_trevor)
            frontmatter_lines.append(f"cover_credits: '{credits}'")

    if hasattr(item, "image") and item.image:
        frontmatter_lines.append(f"image: {item.image.name}")

        full_url = PZT_MEDIA_URL + item.image.name
        frontmatter_lines.append(f"image_full: {full_url}")

        thumbnailer = get_thumbnailer(item.image)
        thumbnail = thumbnailer["imagethumb"]
        frontmatter_lines.append(f"image_thumb: {thumbnail.url}")

        if item.image_url:
            frontmatter_lines.append(f"image_src_url: {item.image_url}")
        if item.image_author:
            frontmatter_lines.append(f"image_author: '{escape(item.image_author)}'")
        if item.image_license:
            frontmatter_lines.append(f"image_license: {item.image_license}")

    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)
    return f"{frontmatter}\n\n{content}"


def create_artist_file_content(item):
    cat_to_str = {
        Artist.CAT_POLISH: "POLISH",
        Artist.CAT_FOREIGN: "FOREIGN",
        Artist.CAT_COMMUNITY: "COMMUNITY",
    }

    frontmatter_lines = ["---"]
    if item.name:
        frontmatter_lines.append(f"name: '{item.name}'")
    if item.featured:
        frontmatter_lines.append(f"featured: '{item.featured}'")
    if item.category and item.category in cat_to_str:
        cat_str = cat_to_str[item.category]
        frontmatter_lines.append(f"category: '{cat_str}'")
    if item.born_on:
        frontmatter_lines.append(f"born_on: '{item.born_on}'")
    if item.died_on:
        frontmatter_lines.append(f"died_on: '{item.died_on}'")

    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)
    return frontmatter


def freeze_song_calendar():
    notes = (
        SongNote.objects.filter(date__isnull=False)
        .exclude(date_description="")
        .order_by("-date")
    )

    frontmatter_lines = []
    frontmatter_lines.append("---")
    frontmatter_lines.append(f"title: 'Historia w piosence'")
    frontmatter_lines.append(f"author: DX")
    cur_datetime = datetime.datetime.now(datetime.timezone.utc)
    frontmatter_lines.append(f"pub_date: '{cur_datetime.isoformat()}'")
    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)

    content_lines = [
        "Piosenki wg. daty wydarzenia historycznego które je zainspirowało:",
        "",
    ]
    for note in notes:
        song_link = f"[{note.song}]({note.song.get_absolute_url()})"
        content_lines.append(
            f' - {note.date.strftime("%d.%m.%Y")}: {song_link}, {note.date_description}'
        )
    content = "\n".join(content_lines)
    return f"{frontmatter}\n\n{content}"


def slugify_with_unidecode(text):
    return slugify(unidecode(text))


class Command(BaseCommand):
    help = "Freezes the db entities as static pages."

    def handle(self, *args, **options):
        for artist in Artist.objects.all():

            dirname = artist.slug
            print(f"Processing: {artist} -> {dirname}")
            item_dir_path = os.path.join(ARTISTS_DIR_PATH, dirname)
            os.makedirs(item_dir_path, exist_ok=True)
            file_path = os.path.join(item_dir_path, "index.md")

            content = create_artist_file_content(artist)
            with open(file_path, "w") as file:
                file.write(content)

            for note in ArtistNote.objects.filter(artist=artist):
                slug = slugify_with_unidecode(note.title)
                file_path = os.path.join(item_dir_path, slug + ".md")
                print(f"  Adding a note: {slug}")
                markdown_text = trevor_to_md(note.text_trevor)
                content = create_file_content(note, markdown_text)
                with open(file_path, "w") as file:
                    file.write(content)

        for song in Song.objects.all():
            # TODO: freeze contributions -> links to relevant artists
            dirname = song.slug
            print(f"Processing: {song} -> {dirname}")
            item_dir_path = os.path.join(SONGS_DIR_PATH, dirname)
            os.makedirs(item_dir_path, exist_ok=True)
            file_path = os.path.join(item_dir_path, "index.md")

            content = create_file_content(song, song.lyrics)
            with open(file_path, "w") as file:
                file.write(content)

            for note in SongNote.objects.filter(song=song):
                slug = slugify_with_unidecode(note.title)
                file_path = os.path.join(item_dir_path, slug + ".md")
                print(f"  Adding a note: {slug}")
                markdown_text = trevor_to_md(note.text_trevor)
                content = create_file_content(note, markdown_text)
                with open(file_path, "w") as file:
                    file.write(content)

        # dir_path = os.path.join(ROOT_PATH, "pages", "artykuly", "historia-w-piosence")
        # os.makedirs(dir_path, exist_ok=True)

        # file_path = os.path.join(dir_path, "index.md")
        # content = freeze_song_calendar()
        # with open(file_path, "w") as file:
        #     file.write(content)
