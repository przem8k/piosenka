import os
from datetime import datetime

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Template, loader
from markdown2 import markdown

from bs4 import BeautifulSoup

PAGES = ["o-stronie"]

ARTICLE_DIR = "artykuly"
BLOG_DIR = "blog"

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


def make_context_for_page(frontmatter_data, content_markdown, section=None):
    content_html = markdown(content_markdown, extras=["break-on-newline"])

    context_data = {
        "title": frontmatter_data.get("title"),
        "content_html": content_html,
        "user_data": {"is_logged_in": False},
        "section": section,
        "cover_url": frontmatter_data.get("cover_image_thumb_600_300"),
        "pub_date": frontmatter_data.get("pub_date"),
        "author": frontmatter_data.get("author"),
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

            context = make_context_for_page(frontmatter_data, content)
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

            context = make_context_for_page(
                frontmatter_data, content, section="articles"
            )
            write_page(context, "page.html", out_file_path)

            slug = os.path.relpath(subdir, article_dir_path).strip("/")
            articles.append(make_context_item_for_article_index(slug, frontmatter_data, content))
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

            context = make_context_for_page(
                frontmatter_data, content, section="blog"
            )
            write_page(context, "page.html", out_file_path)
            
            slug = os.path.relpath(subdir, article_dir_path).strip("/")
            posts.append(make_context_item_for_post_index(slug, frontmatter_data, content))
        posts.sort(key=lambda x: x["pub_date"], reverse=True)
        context = {
            "all_posts": posts,
            "new_posts": posts[:5],
            "user_data": {"is_logged_in": False},
        }
        out_file_path = os.path.join(OUT_DIR_PATH, BLOG_DIR, "index.html")
        write_page(context, "blog/index.html", out_file_path)