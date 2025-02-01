import os
from datetime import datetime
import json

import yaml
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Template, loader
from markdown2 import markdown

from piosenka import lyrics

PAGES = {
    "o-stronie": "page.html",
    "szukaj": "search.html",
}

ARTICLE_DIR = "artykuly"
BLOG_DIR = "blog"
SONGS_DIR = "opracowanie"
ARTISTS_DIR = "spiewnik"

CONTENT_DIR = "pages"
OUT_DIR = "out"

ROOT_PATH = os.path.abspath(os.path.join(__file__, "../../../.."))
OUT_DIR_PATH = os.path.join(ROOT_PATH, OUT_DIR)
CONTENT_PATH = os.path.join(ROOT_PATH, CONTENT_DIR)
ARTISTS_DIR_PATH = os.path.join(CONTENT_PATH, ARTISTS_DIR)


def parse_file(src_path):
    with open(src_path, "r") as file:
        lines = file.readlines()

        frontmatter, content = "".join(lines).split("---")[1:3]
        frontmatter_data = yaml.safe_load(frontmatter)

        if "pub_date" in frontmatter_data:
            frontmatter_data["pub_date"] = datetime.fromisoformat(
                frontmatter_data["pub_date"]
            )
        if "born_on" in frontmatter_data:
            frontmatter_data["born_on"] = datetime.fromisoformat(
                frontmatter_data["born_on"]
            ).date()
        if "died_on" in frontmatter_data:
            frontmatter_data["died_on"] = datetime.fromisoformat(
                frontmatter_data["died_on"]
            ).date()
        return (frontmatter_data, content)


CAPO_TO_ROMAN = [
    "",
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
]


def capo_to_roman(capo_fret):
    if capo_fret:
        return CAPO_TO_ROMAN[capo_fret]
    else:
        return None


def make_context_for_page(frontmatter_data, section=None):
    context_data = {
        "title": frontmatter_data.get("title"),
        "user_data": {"is_logged_in": False},
        "section": section,
        "cover_url": frontmatter_data.get("cover_image_thumb_600_300"),
        "pub_date": frontmatter_data.get("pub_date"),
        "author": frontmatter_data.get("author"),
        # Song-specific:
        "original_title": frontmatter_data.get("original_title"),
        "disambig": frontmatter_data.get("disambig"),
        "text_authors": frontmatter_data.get("text_authors"),
        "composers": frontmatter_data.get("composers"),
        "translators": frontmatter_data.get("translators"),
        "performers": frontmatter_data.get("performers"),
        "capo_fret": capo_to_roman(frontmatter_data.get("capo_fret")),
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
        "filter_epigone": frontmatter_data.get("died_on"),
        # Article-specific:
        "lead": frontmatter_data.get("lead"),
    }

    if context_data["disambig"]:
        context_data["title"] += f" ({context_data['disambig']})"

    if "cover_credits" in frontmatter_data:
        cover_credits_html = markdown(frontmatter_data.get("cover_credits"))
        context_data["cover_credits_html"] = cover_credits_html

    return context_data


def add_lead(context, content_html, lead_max_len=200):
    # Extract text, removing all tags
    soup = BeautifulSoup(content_html, "html.parser")
    content_text = soup.get_text(separator=" ", strip=True)

    lead_html = content_text[:lead_max_len]
    read_more = False
    if len(content_text) > lead_max_len:
        last_space = lead_html.rfind(" ")
        if last_space != -1:
            lead_html = lead_html[:last_space]
        lead_html += "..."
        read_more = True

    context["lead_html"] = lead_html
    context["read_more"] = read_more


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


def generate_pages():
    for page, template in PAGES.items():
        src_path = os.path.join(CONTENT_PATH, page, "index.md")
        frontmatter_data, content = parse_file(src_path)

        out_dir = os.path.join(OUT_DIR_PATH, page)
        os.makedirs(out_dir, exist_ok=True)
        out_file_path = os.path.join(out_dir, "index.html")

        context = make_context_for_page(frontmatter_data)
        context["content_html"] = markdown(content, extras=["break-on-newline"])
        write_page(context, template, out_file_path)


def generate_articles():
    article_dir_path = os.path.join(CONTENT_PATH, ARTICLE_DIR)
    articles = []
    for subdir, _, _ in os.walk(article_dir_path):
        index_md_path = os.path.join(subdir, "index.md")
        if not os.path.exists(index_md_path):
            continue
        frontmatter_data, content = parse_file(index_md_path)

        out_dir = os.path.join(OUT_DIR_PATH, os.path.relpath(subdir, CONTENT_PATH))
        os.makedirs(out_dir, exist_ok=True)
        out_file_path = os.path.join(out_dir, "index.html")

        article_context = make_context_for_page(frontmatter_data, section="articles")
        content_html = markdown(content, extras=["break-on-newline"])
        article_context["content_html"] = content_html
        article_slug = os.path.relpath(subdir, article_dir_path).strip("/")
        article_context["get_absolute_url"] = f"/artykuly/{article_slug}/"
        article_context["thumb_url"] = frontmatter_data.get("cover_image_thumb_420_210")

        if article_context["lead"]:
            article_context["lead_html"] = markdown(article_context["lead"])
        else:
            add_lead(article_context, content_html, 200)

        write_page(article_context, "page.html", out_file_path)
        articles.append(article_context)
    articles.sort(key=lambda x: x["pub_date"], reverse=True)
    context = {
        "articles": articles,
        "user_data": {"is_logged_in": False},
    }
    out_file_path = os.path.join(OUT_DIR_PATH, ARTICLE_DIR, "index.html")
    write_page(context, "articles/index.html", out_file_path)
    return articles


def generate_posts():
    blog_dir_path = os.path.join(CONTENT_PATH, BLOG_DIR)
    posts = []
    for subdir, _, _ in os.walk(blog_dir_path):
        index_md_path = os.path.join(subdir, "index.md")
        if not os.path.exists(index_md_path):
            continue
        frontmatter_data, content = parse_file(index_md_path)

        out_dir = os.path.join(OUT_DIR_PATH, os.path.relpath(subdir, CONTENT_PATH))
        os.makedirs(out_dir, exist_ok=True)
        out_file_path = os.path.join(out_dir, "index.html")

        content_html = markdown(content, extras=["break-on-newline"])
        post_context = make_context_for_page(frontmatter_data, section="blog")
        post_context["content_html"] = content_html
        post_slug = os.path.relpath(subdir, blog_dir_path).strip("/")
        post_context["get_absolute_url"] = f"/blog/{post_slug}/"
        add_lead(post_context, content_html, 500)

        write_page(post_context, "page.html", out_file_path)
        posts.append(post_context)
    posts.sort(key=lambda x: x["pub_date"], reverse=True)
    context = {
        "all_posts": posts,
        "new_posts": posts[:5],
        "user_data": {"is_logged_in": False},
    }
    out_file_path = os.path.join(OUT_DIR_PATH, BLOG_DIR, "index.html")
    write_page(context, "blog/index.html", out_file_path)
    return posts


def parse_artists():
    artists_by_slug = {}
    for subdir, _, _ in os.walk(ARTISTS_DIR_PATH):
        index_md_path = os.path.join(subdir, "index.md")
        if not os.path.exists(index_md_path):
            continue
        frontmatter_data, content = parse_file(index_md_path)
        artist_slug = os.path.relpath(subdir, ARTISTS_DIR_PATH).strip("/")
        artist = make_context_for_page(frontmatter_data, section="songs")
        artist["get_absolute_url"] = f"/spiewnik/{artist_slug}/"
        artists_by_slug[artist_slug] = artist
    return artists_by_slug


def generate_songs(artists_by_slug):
    songs_by_artist_slug = {}

    songs_dir_path = os.path.join(CONTENT_PATH, SONGS_DIR)
    song_notes = []
    for subdir, _, _ in os.walk(songs_dir_path):
        index_md_path = os.path.join(subdir, "index.md")
        if not os.path.exists(index_md_path):
            continue
        frontmatter_data, content = parse_file(index_md_path)
        song_slug = os.path.relpath(subdir, songs_dir_path).strip("/")

        out_dir = os.path.join(OUT_DIR_PATH, os.path.relpath(subdir, CONTENT_PATH))
        os.makedirs(out_dir, exist_ok=True)
        out_file_path = os.path.join(out_dir, "index.html")

        content_html = lyrics.render_lyrics(content)
        context = make_context_for_page(frontmatter_data, section="songs")
        context["content_html"] = content_html
        context["get_absolute_url"] = f"/opracowanie/{song_slug}/"
        artist_slugs = set(
            (context["text_authors"] if context["text_authors"] else [])
            + (context["composers"] if context["composers"] else [])
            + (context["translators"] if context["translators"] else [])
            + (context["performers"] if context["performers"] else [])
        )
        for artist_slug in artist_slugs:
            if artist_slug not in songs_by_artist_slug:
                songs_by_artist_slug[artist_slug] = []
            songs_by_artist_slug[artist_slug].append(context)
        context["text_authors"] = make_artist_list(
            artists_by_slug, context["text_authors"]
        )
        context["composers"] = make_artist_list(artists_by_slug, context["composers"])
        context["translators"] = make_artist_list(
            artists_by_slug, context["translators"]
        )
        context["performers"] = make_artist_list(artists_by_slug, context["performers"])

        notes = []
        for root, _, files in os.walk(subdir):
            for file in files:
                if file == "index.md" or not file.endswith(".md"):
                    continue
                file_path = os.path.join(root, file)
                print(f"{file_path}")
                note_frontmatter_data, note_content = parse_file(file_path)
                note_content_html = markdown(note_content, extras=["break-on-newline"])
                note_context = make_context_for_page(
                    note_frontmatter_data, section="songs"
                )
                note_context["content_html"] = note_content_html
                note_context["song"] = context
                notes.append(note_context)

        context["notes"] = notes
        context["num_notes"] = len(notes)
        write_page(context, "songs/song.html", out_file_path)

        song_notes += notes
    return songs_by_artist_slug, song_notes


def generate_songbook_index(artists_by_slug):
    hero_artists = [
        artists_by_slug["jacek-kaczmarski"],
        artists_by_slug["przemyslaw-gintrowski"],
        artists_by_slug["kaczmarski-gintrowski-lapinski"],
        artists_by_slug["pawel-wojcik"],
        artists_by_slug["jacek-kowalski"],
        artists_by_slug["mariusz-zadura"],
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
    return song_index_context


def generate_artists(artists_by_slug, songs_by_artist_slug, song_index_context):
    for artist_slug, artist_context in artists_by_slug.items():
        if not artist_context["featured"]:
            continue

        subdir = os.path.join(ARTISTS_DIR_PATH, artist_slug)
        notes = []
        for root, _, files in os.walk(subdir):
            for file in files:
                if file == "index.md" or not file.endswith(".md"):
                    continue
                file_path = os.path.join(root, file)
                print(f"{file_path}")
                note_frontmatter_data, note_content = parse_file(file_path)
                note_content_html = markdown(note_content, extras=["break-on-newline"])
                note_context = make_context_for_page(
                    note_frontmatter_data, section="songs"
                )
                note_context["content_html"] = note_content_html
                notes.append(note_context)
        out_dir = os.path.join(OUT_DIR_PATH, os.path.relpath(subdir, CONTENT_PATH))
        os.makedirs(out_dir, exist_ok=True)
        out_file_path = os.path.join(out_dir, "index.html")

        songs = songs_by_artist_slug[artist_slug]
        songs.sort(key=lambda x: x["title"])

        if artist_context["filter_epigone"]:
            filtered_songs = [song for song in songs if not song.get("epigone")]
            epigone_songs = [song for song in songs if song.get("epigone")]
        else:
            filtered_songs = songs
            epigone_songs = []

        artist_context["songs"] = filtered_songs
        artist_context["epigone_songs"] = epigone_songs

        notes.sort(key=lambda x: x["pub_date"], reverse=True)
        artist_context["notes"] = notes
        artist_context.update(song_index_context)
        write_page(artist_context, "songs/artist.html", out_file_path)


def generate_artist_index(artists_by_slug):
    resp = []
    for artist_slug, artist in artists_by_slug.items():
        if not "featured" in artist or not artist["featured"]:
            continue
        resp.append(
            {
                "name": artist["name"],
                "value": artist["name"],
                "tokens": artist["name"].split(),
                "url": artist["get_absolute_url"],
            }
        )
    out_dir_path = os.path.join(OUT_DIR_PATH, "index")
    out_file_path = os.path.join(out_dir_path, "artists.json")
    os.makedirs(out_dir_path, exist_ok=True)
    with open(out_file_path, "w") as f:
        json.dump(resp, f, ensure_ascii=False, indent=4)


def generate_song_index(all_songs):
    resp = []
    for song in all_songs:
        resp.append(
            {
                "name": song["title"],
                "value": song["title"],
                "tokens": song["title"].split(),
                "url": song["get_absolute_url"],
            }
        )
    out_dir_path = os.path.join(OUT_DIR_PATH, "index")
    out_file_path = os.path.join(out_dir_path, "songs.json")
    os.makedirs(out_dir_path, exist_ok=True)
    with open(out_file_path, "w") as f:
        json.dump(resp, f, ensure_ascii=False, indent=4)


class Command(BaseCommand):
    help = "Generates the static pages."

    def handle(self, *args, **options):
        generate_pages()

        articles = generate_articles()
        articles.sort(key=lambda x: x["pub_date"], reverse=True)
        posts = generate_posts()
        artists_by_slug = parse_artists()
        songs_by_artist_slug, song_notes = generate_songs(artists_by_slug)
        songbook_index_context = generate_songbook_index(artists_by_slug)
        generate_artists(artists_by_slug, songs_by_artist_slug, songbook_index_context)

        all_songs = {}
        for artist_songs in songs_by_artist_slug.values():
            for song in artist_songs:
                all_songs[song["get_absolute_url"]] = song
        all_songs = list(all_songs.values())
        all_songs.sort(key=lambda x: x["pub_date"], reverse=True)

        song_notes.sort(key=lambda x: x["pub_date"], reverse=True)

        frontpage_context = {
            "post": posts[0],
            "note": song_notes[0],
            "songs": all_songs[:10],
            "notes": song_notes[:10],
            "article": articles[0],
        }

        private_gen_vars_path = os.path.join(ROOT_PATH, "private_gen_vars.yaml")
        with open(private_gen_vars_path, "r") as file:
            private_gen_vars = yaml.safe_load(file)
        frontpage_context["calendar_api_key"] = private_gen_vars["calendar_api_key"]
        out_file_path = os.path.join(OUT_DIR_PATH, "index.html")
        write_page(frontpage_context, "frontpage/index.html", out_file_path)

        generate_artist_index(artists_by_slug)
        generate_song_index(all_songs)