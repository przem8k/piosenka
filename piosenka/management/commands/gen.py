import os

from django.core.management.base import BaseCommand
from django.template import Context, Template, loader
from django.conf import settings
import yaml
from markdown2 import markdown

PAGES = [
    "o-stronie"
]

CONTENT_DIR = "pages"
OUT_DIR = "out"

ROOT_PATH = os.path.abspath(os.path.join(__file__, "../../../.."))


def process_single_page(src_path, out_file):
    with open(src_path, 'r') as file:
        lines = file.readlines()

        frontmatter, markdown_content = ''.join(lines).split('---')[1:3]
        frontmatter_data = yaml.safe_load(frontmatter)
        html_content = markdown(markdown_content)
 
        context_data = {
            'title': frontmatter_data['title'],
            'content': html_content,
            'user_data': {
                'is_logged_in': False
            }
        }

        template = loader.get_template('page.html')
        rendered_template = template.render(context_data)

        with open(out_file, 'w') as f:
            f.write(rendered_template)


class Command(BaseCommand):
    help = "Generates the static pages."

    def handle(self, *args, **options):
        for page in PAGES:
            src_path = os.path.join(ROOT_PATH, CONTENT_DIR, page, "index.md")
            out_dir = os.path.join(ROOT_PATH, OUT_DIR, page)
            os.makedirs(out_dir, exist_ok=True)
            out_file = os.path.join(out_dir, "index.html")
            print(f'out: {out_file}')
            process_single_page(src_path, out_file)