"""Freezes the db entities as static pages."""

import os
import datetime

from songs.models import Song, SongNote
from django.core.management.base import BaseCommand
from easy_thumbnails.files import get_thumbnailer

from content.trevor import trevor_to_md

PAGES = ["o-stronie"]

CONTENT_DIR = "pages"

ROOT_PATH = os.path.abspath(os.path.join(__file__, "../../../.."))

BLOG_DIR_PATH = os.path.join(ROOT_PATH, "pages", "blog")

PZT_MEDIA_URL = "https://storage.googleapis.com/piosenka-media/media/"


def create_file_content(item, markdown_text):
    frontmatter_lines = ["---"]
    if item.title:
        frontmatter_lines.append(f"title: '{item.title}'")
    if item.author:
        frontmatter_lines.append(f"author: {item.author}")
    if item.pub_date:
        frontmatter_lines.append(f"pub_date: '{item.pub_date}'")
    if hasattr(item, 'cover_image') and item.cover_image:
        frontmatter_lines.append(f"cover_image: {item.cover_image.name}")
        full_url = PZT_MEDIA_URL + item.cover_image.name
        frontmatter_lines.append(f"cover_image_full: {full_url}")

        thumbnailer = get_thumbnailer(item.cover_image)
        thumbnail_cover = thumbnailer["cover"]
        frontmatter_lines.append(f"cover_image_thumb_600_300: {thumbnail_cover.url}")
        thumbnail_mini = thumbnailer["coverthumb"]
        frontmatter_lines.append(f"cover_image_thumb_420_210: {thumbnail_mini.url}")
    if hasattr(item, 'cover_credits_trevor') and item.cover_credits_trevor:
        credits = trevor_to_md(item.cover_credits_trevor)
        frontmatter_lines.append(f"cover_credits: '{credits}'")

    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)
    return f"{frontmatter}\n\n{markdown_text}"


def freeze_song_calendar():
    notes = (
        SongNote.objects
        .filter(date__isnull=False)
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

    content_lines = ['Piosenki wg. daty wydarzenia historycznego które je zainspirowało:', '']
    for note in notes:
        song_link = f"[{note.song}]({note.song.get_absolute_url()})"
        content_lines.append(f' - {note.date.strftime("%d.%m.%Y")}: {song_link}, {note.date_description}')
    content = "\n".join(content_lines)
    return f"{frontmatter}\n\n{content}"



class Command(BaseCommand):
    help = "Freezes the db entities as static pages."

    def handle(self, *args, **options):
        # for post in Post.objects.all():

        #     dirname = post.slug
        #     print(f"Processing: {post} -> {dirname}")
        #     item_dir_path = os.path.join(BLOG_DIR_PATH, dirname)
        #     os.makedirs(item_dir_path, exist_ok=True)
        #     file_path = os.path.join(item_dir_path, "index.md")

        #     markdown_text = trevor_to_md(post.post_trevor)
        #     if post.more_trevor:
        #         markdown_text += "\n\n"
        #         markdown_text += trevor_to_md(post.more_trevor)

        #     content = create_file_content(post, markdown_text)
        #     with open(file_path, "w") as file:
        #         file.write(content)

                #     dirname = post.slug
        #     print(f"Processing: {post} -> {dirname}")
        #     item_dir_path = os.path.join(BLOG_DIR_PATH, dirname)
        #     os.makedirs(item_dir_path, exist_ok=True)
        #     file_path = os.path.join(item_dir_path, "index.md")

        dir_path = os.path.join(ROOT_PATH, "pages", "artykuly", "historia-w-piosence")
        os.makedirs(dir_path, exist_ok=True)

        file_path = os.path.join(dir_path, "index.md")
        content = freeze_song_calendar()
        with open(file_path, "w") as file:
            file.write(content)