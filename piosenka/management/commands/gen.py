import os
from datetime import datetime

import yaml
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Template, loader
from markdown2 import markdown

from songs import lyrics

PAGES = ["o-stronie"]

ARTICLE_DIR = "artykuly"
BLOG_DIR = "blog"
SONGS_DIR = "opracowanie"
ARTISTS_DIR = "spiewnik"

CONTENT_DIR = "pages"
OUT_DIR = "out"

ROOT_PATH = os.path.abspath(os.path.join(__file__, "../../../.."))
OUT_DIR_PATH = os.path.join(ROOT_PATH, OUT_DIR)


def parse_file(src_path):
    with open(src_path, "r") as file:
        lines = file.readlines()

        frontmatter, content = "".join(lines).split("---")[1:3]
        frontmatter_data = yaml.safe_load(frontmatter)

        if "pub_date" in frontmatter_data:
            frontmatter_data["pub_date"] = datetime.fromisoformat(
                frontmatter_data["pub_date"]
            )
        return (frontmatter_data, content)


def make_context_for_page(frontmatter_data, content_html, section=None):
    context_data = {
        "title": frontmatter_data.get("title"),
        "content_html": content_html,
        "user_data": {"is_logged_in": False},
        "section": section,
        "cover_url": frontmatter_data.get("cover_image_thumb_600_300"),
        "pub_date": frontmatter_data.get("pub_date"),
        "author": frontmatter_data.get("author"),
        # Song-specific:
        "original_title": frontmatter_data.get("original_title"),
        "text_authors": frontmatter_data.get("text_authors"),
        "composers": frontmatter_data.get("composers"),
        "translators": frontmatter_data.get("translators"),
        "performers": frontmatter_data.get("performers"),
        "capo": frontmatter_data.get("capo_fret"),
        "youtube_id": frontmatter_data.get("youtube_id"),
        "epigone": frontmatter_data.get("epigone"),
        # Note-specific:
        "url1": frontmatter_data.get("url1"),
        "url2": frontmatter_data.get("url2"),
        "ref1": frontmatter_data.get("ref1"),
        "ref2": frontmatter_data.get("ref2"),
        "ref2": frontmatter_data.get("ref2"),
        "image_full": frontmatter_data.get("image_full"),
        "image_thumb": frontmatter_data.get("image_thumb"),
        "score1_full": frontmatter_data.get("score1_full"),
        "score1_thumb": frontmatter_data.get("score1_thumb"),
        "score2_full": frontmatter_data.get("score2_full"),
        "score2_thumb": frontmatter_data.get("score2_thumb"),
        "score3_full": frontmatter_data.get("score3_full"),
        "score3_thumb": frontmatter_data.get("score3_thumb"),
        "image_src_url": frontmatter_data.get("image_src_url"),
        "image_author": frontmatter_data.get("image_author"),
        "image_license": frontmatter_data.get("image_license"),
        # Artist-specific:
        "name": frontmatter_data.get("name"),
        "featured": frontmatter_data.get("featured"),
        "category": frontmatter_data.get("category"),
        "born_on": frontmatter_data.get("born_on"),
        "died_on": frontmatter_data.get("died_on"),
    }

    if "cover_credits" in frontmatter_data:
        cover_credits_html = markdown(frontmatter_data.get("cover_credits"))
        context_data["cover_credits_html"] = cover_credits_html

    return context_data


def make_context_item_for_article_index(slug, frontmatter_data, content_markdown):
    content_html = markdown(content_markdown, extras=["strip"])
    # Extract text, removing all tags
    soup = BeautifulSoup(content_html, "html.parser")
    content_text = soup.get_text(separator=" ", strip=True)

    lead = content_text[:200]
    if len(content_text) > 200:
        last_space = lead.rfind(" ")
        if last_space != -1:
            lead = lead[:last_space]
        lead += "..."
    res = {
        "title": frontmatter_data.get("title"),
        "get_absolute_url": f"/artykuly/{slug}/",
        "lead_html": lead,
        "thumb_url": frontmatter_data.get("cover_image_thumb_420_210"),
        "pub_date": frontmatter_data.get("pub_date"),
    }
    return res


def make_context_item_for_post_index(slug, frontmatter_data, content_markdown):
    content_text = markdown(content_markdown, extras=["strip"])
    lead = content_text[:500]
    read_more = False
    if len(content_text) > 500:
        last_space = lead.rfind(" ")
        if last_space != -1:
            lead = lead[:last_space]
        lead += "..."
        read_more = True
    res = {
        "title": frontmatter_data.get("title"),
        "get_absolute_url": f"/blog/{slug}/",
        "lead_html": lead,
        "read_more": read_more,
        "pub_date": frontmatter_data.get("pub_date"),
        "author": frontmatter_data.get("author"),
    }
    return res


def write_page(context_data, template, out_file):
    template = loader.get_template(template)
    rendered_template = template.render(context_data)

    with open(out_file, "w") as f:
        f.write(rendered_template)


def make_artist_list(artists_by_slug, artist_slugs):
    ret = []
    if not artist_slugs:
        return ret

    for artist_slug in artist_slugs:
        assert artist_slug in artist_slugs
        artist = artists_by_slug[artist_slug]
        ret.append(artist)
    return ret

class Command(BaseCommand):
    help = "Generates the static pages."

    def handle(self, *args, **options):
        content_path = os.path.join(ROOT_PATH, CONTENT_DIR)
        for page in PAGES:
            src_path = os.path.join(content_path, page, "index.md")
            frontmatter_data, content = parse_file(src_path)

            out_dir = os.path.join(OUT_DIR_PATH, page)
            os.makedirs(out_dir, exist_ok=True)
            out_file_path = os.path.join(out_dir, "index.html")

            content_html = markdown(content, extras=["break-on-newline"])
            context = make_context_for_page(frontmatter_data, content_html)
            write_page(context, "page.html", out_file_path)

        article_dir_path = os.path.join(content_path, ARTICLE_DIR)
        articles = []
        for subdir, _, _ in os.walk(article_dir_path):
            index_md_path = os.path.join(subdir, "index.md")
            if not os.path.exists(index_md_path):
                continue
            frontmatter_data, content = parse_file(index_md_path)

            out_dir = os.path.join(OUT_DIR_PATH, os.path.relpath(subdir, content_path))
            os.makedirs(out_dir, exist_ok=True)
            out_file_path = os.path.join(out_dir, "index.html")

            content_html = markdown(content, extras=["break-on-newline"])
            context = make_context_for_page(
                frontmatter_data, content_html, section="articles"
            )
            write_page(context, "page.html", out_file_path)

            slug = os.path.relpath(subdir, article_dir_path).strip("/")
            articles.append(
                make_context_item_for_article_index(slug, frontmatter_data, content)
            )
        articles.sort(key=lambda x: x["pub_date"], reverse=True)
        context = {
            "articles": articles,
            "user_data": {"is_logged_in": False},
        }
        out_file_path = os.path.join(OUT_DIR_PATH, ARTICLE_DIR, "index.html")
        write_page(context, "articles/index.html", out_file_path)

        blog_dir_path = os.path.join(content_path, BLOG_DIR)
        posts = []
        for subdir, _, _ in os.walk(blog_dir_path):
            index_md_path = os.path.join(subdir, "index.md")
            if not os.path.exists(index_md_path):
                continue
            frontmatter_data, content = parse_file(index_md_path)

            out_dir = os.path.join(OUT_DIR_PATH, os.path.relpath(subdir, content_path))
            os.makedirs(out_dir, exist_ok=True)
            out_file_path = os.path.join(out_dir, "index.html")

            content_html = markdown(content, extras=["break-on-newline"])
            context = make_context_for_page(frontmatter_data, content_html, section="blog")
            write_page(context, "page.html", out_file_path)

            slug = os.path.relpath(subdir, blog_dir_path).strip("/")
            posts.append(
                make_context_item_for_post_index(slug, frontmatter_data, content)
            )
        posts.sort(key=lambda x: x["pub_date"], reverse=True)
        context = {
            "all_posts": posts,
            "new_posts": posts[:5],
            "user_data": {"is_logged_in": False},
        }
        out_file_path = os.path.join(OUT_DIR_PATH, BLOG_DIR, "index.html")
        write_page(context, "blog/index.html", out_file_path)

        artists_dir_path = os.path.join(content_path, ARTISTS_DIR)
        artists_by_slug = {}
        songs_by_artist_slug = {}
        for subdir, _, _ in os.walk(artists_dir_path):
            index_md_path = os.path.join(subdir, "index.md")
            if not os.path.exists(index_md_path):
                continue
            frontmatter_data, content = parse_file(index_md_path)
            artist_slug = os.path.relpath(subdir, artists_dir_path).strip("/")
            artist = make_context_for_page(frontmatter_data, "", section="songs")
            artist["get_absolute_url"] = f'/spiewnik/{artist_slug}/'
            artists_by_slug[artist_slug] = artist
            songs_by_artist_slug[artist_slug] = []

        songs_dir_path = os.path.join(content_path, SONGS_DIR)
        songs = []
        for subdir, _, _ in os.walk(songs_dir_path):
            index_md_path = os.path.join(subdir, "index.md")
            if not os.path.exists(index_md_path):
                continue
            frontmatter_data, content = parse_file(index_md_path)
            song_slug = os.path.relpath(subdir, songs_dir_path).strip("/")

            notes = []
            for root, _, files in os.walk(subdir):
                for file in files:
                    if file == "index.md" or not file.endswith(".md"):
                        continue
                    file_path = os.path.join(root, file)
                    print(f'{file_path}')
                    note_frontmatter_data, note_content = parse_file(file_path)
                    note_content_html = markdown(note_content, extras=["break-on-newline"])
                    note_context = make_context_for_page(note_frontmatter_data, note_content_html, section="songs")
                    notes.append(note_context)

            out_dir = os.path.join(OUT_DIR_PATH, os.path.relpath(subdir, content_path))
            os.makedirs(out_dir, exist_ok=True)
            out_file_path = os.path.join(out_dir, "index.html")

            content_html = lyrics.render_lyrics(content)
            context = make_context_for_page(frontmatter_data, content_html, section="songs")
            context["get_absolute_url"] = f'/opracowanie/{song_slug}/'
            artist_slugs = set(
                (context["text_authors"] if context["text_authors"] else []) +
                (context["composers"] if context["composers"] else []) +
                (context["translators"] if context["translators"] else []) +
                (context["performers"] if context["performers"] else [])
            )
            if not context["epigone"]:
                for artist_slug in artist_slugs:
                    songs_by_artist_slug[artist_slug].append(context)
            context["text_authors"] = make_artist_list(artists_by_slug, context["text_authors"])
            context["composers"] = make_artist_list(artists_by_slug, context["composers"])
            context["translators"] = make_artist_list(artists_by_slug, context["translators"])
            context["performers"] = make_artist_list(artists_by_slug, context["performers"])
            context["notes"] = notes
            context["num_notes"] = len(notes)
            write_page(context, "songs/song.html", out_file_path)

        hero_artists = [
            artists_by_slug["jacek-kaczmarski"],
            artists_by_slug["jacek-kaczmarski"],
            artists_by_slug["jacek-kaczmarski"],
            artists_by_slug["jacek-kaczmarski"],
            artists_by_slug["jacek-kaczmarski"],
            artists_by_slug["jacek-kaczmarski"],
        ]

        polish_artists = []
        foreign_artists = []
        community_artists = []
        for artist_slug, artist in artists_by_slug.items():
            if not artist["featured"]:
                continue

            if artist["category"] == "POLISH":
                polish_artists.append(artist)
            elif artist["category"] == "FOREIGN":
                foreign_artists.append(artist)
            elif artist["category"] == "COMMUNITY":
                community_artists.append(artist)

        polish_artists.sort(key=lambda x: x["name"])
        foreign_artists.sort(key=lambda x: x["name"])
        community_artists.sort(key=lambda x: x["name"])

        song_index_context = {
            "hero_artists": hero_artists,
            "polish": polish_artists,
            "foreign": foreign_artists,
            "community": community_artists,
        }
        out_dir = os.path.join(OUT_DIR_PATH, ARTISTS_DIR)
        os.makedirs(out_dir, exist_ok=True)
        out_file_path = os.path.join(out_dir, "index.html")
        write_page(song_index_context, "songs/index.html", out_file_path)

        for subdir, _, _ in os.walk(artists_dir_path):
            index_md_path = os.path.join(subdir, "index.md")
            if not os.path.exists(index_md_path):
                continue
            frontmatter_data, content = parse_file(index_md_path)
            artist_slug = os.path.relpath(subdir, artists_dir_path).strip("/")

            notes = []
            for root, _, files in os.walk(subdir):
                for file in files:
                    if file == "index.md" or not file.endswith(".md"):
                        continue
                    file_path = os.path.join(root, file)
                    print(f'{file_path}')
                    note_frontmatter_data, note_content = parse_file(file_path)
                    note_content_html = markdown(note_content, extras=["break-on-newline"])
                    note_context = make_context_for_page(note_frontmatter_data, note_content_html, section="songs")
                    notes.append(note_context)
            out_dir = os.path.join(OUT_DIR_PATH, os.path.relpath(subdir, content_path))
            os.makedirs(out_dir, exist_ok=True)
            out_file_path = os.path.join(out_dir, "index.html")

            context = make_context_for_page(frontmatter_data, "", section="songs")
            songs = songs_by_artist_slug[artist_slug]
            songs.sort(key=lambda x: x["title"])
            context["songs"] = songs
            context["notes"] = notes
            write_page(context, "songs/artist.html", out_file_path)