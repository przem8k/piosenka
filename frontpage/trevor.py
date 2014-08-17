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
        else:
            raise RuntimeError("Cannot render an unsupported sirtrevor block.")

    return output

def text_block(data):
    return markdown(data['text'], safe_mode='escape')

def list_block(data):
    return markdown(data['text'], safe_mode='escape')

def put_text_in_trevor(text):
    return json.dumps({
        'data': [{
            'type': "text",
            'data': {
                'text': text
            }
        }]
    })
