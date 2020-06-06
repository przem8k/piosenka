import json

import markdown
import bleach


def render_trevor(trevor_data):
    parsed = json.loads(trevor_data)
    output = ''

    for block in parsed['data']:
        if block['type'] == 'text':
            output += text_block(block['data'])
        elif block['type'] == 'list':
            output += list_block(block['data'])
        elif block['type'] == 'quote':
            output += quote_block(block['data'])
        elif block['type'] == 'heading':
            output += heading_block(block['data'])
        else:
            raise RuntimeError('Cannot render an unsupported sirtrevor block.')

    return output


def text_block(data):
    return _render_markdown(data['text'])


def list_block(data):
    return _render_markdown(data['text'])


def quote_block(data):
    unique_tag = 'ThisIsAUniqueTag'
    # Append the tag before line breaks.
    text = data['text'].replace('\n', unique_tag + '\n')
    return _render_markdown(
        text).replace(unique_tag, '<br />')


def heading_block(data):
    return '<h2>' + _render_markdown(data['text']) + '</h2>'


def put_text_in_trevor(text):
    return json.dumps({'data': [{'type': 'text', 'data': {'text': text}}]})

def _render_markdown(text):
    html = markdown.markdown(text)
    return bleach.clean(html)