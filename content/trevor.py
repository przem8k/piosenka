import json

from markdown import markdown


def render_trevor(trevor_data):
    parsed = json.loads(trevor_data)
    output = str()

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
    return markdown(data['text'], safe_mode='escape')


def list_block(data):
    return markdown(data['text'], safe_mode='escape')


def quote_block(data):
    crazy_unique_tag = 'CrazyUniqueTag'
    # Append the tag before line breaks.
    text = data['text'].replace('\n', crazy_unique_tag + '\n')
    return markdown(
        text, safe_mode='escape').replace(crazy_unique_tag, '<br />')


def heading_block(data):
    return '<h2>' + markdown(data['text'], safe_mode='escape') + '</h2>'


def put_text_in_trevor(text):
    return json.dumps({'data': [{'type': 'text', 'data': {'text': text}}]})
