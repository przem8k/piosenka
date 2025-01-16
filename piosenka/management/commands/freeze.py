"""Freezes the db entities as static pages."""

import os

from django.core.management.base import BaseCommand

from articles.models import Article
from content.trevor import trevor_to_md

PAGES = [
    'o-stronie'
]

CONTENT_DIR = 'pages'

ROOT_PATH = os.path.abspath(os.path.join(__file__, '../../../..'))

ARTICLES_DIR_PATH = os.path.join(ROOT_PATH, 'pages', 'artykuly')

PZT_MEDIA_URL = 'https://storage.googleapis.com/piosenka-media/media/'

def create_file_content(item, markdown_text):
    frontmatter_lines = ['---']
    if item.title:
        frontmatter_lines.append(f'title: {item.title}')
    if item.author:
        frontmatter_lines.append(f'author: {item.author}')
    if item.pub_date:
        frontmatter_lines.append(f'pub_date: {item.pub_date}')
    if item.cover_image:
        url = PZT_MEDIA_URL + item.cover_image.name
        frontmatter_lines.append(f'cover_image: {url}')
    # TODO: handle thumbnails, add cover credits
    frontmatter_lines.append('---')
    frontmatter = '\n'.join(frontmatter_lines)
    return f'{frontmatter}\n\n{markdown_text}'

class Command(BaseCommand):
    help = 'Freezes the db entities as static pages.'

    def handle(self, *args, **options):
        for article in Article.objects.all():
            
            dirname = article.slug
            print(f'Processing: {article} -> {dirname}')
            item_dir_path = os.path.join(ARTICLES_DIR_PATH, dirname)
            os.makedirs(item_dir_path, exist_ok=True)
            file_path = os.path.join(item_dir_path, 'index.md')

            markdown_text = trevor_to_md(article.lead_text_trevor) + '\n\n' + trevor_to_md(article.main_text_trevor)

            print(article)
            for field in article._meta.fields:
                print(f"{field.name}")
            print(f"{article.cover_image}")
            content = create_file_content(article, markdown_text)
            with open(file_path, 'w') as file:
                file.write(content)