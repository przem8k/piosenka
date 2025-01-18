import json

import bleach
import markdown

_BLEACH_ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "em",
    "i",
    "li",
    "ol",
    "p",
    "strong",
    "ul",
]


def render_trevor(trevor_data):
    parsed = json.loads(trevor_data)
    output = ""

    for block in parsed["data"]:
        if block["type"] == "text":
            output += _text_block(block["data"])
        elif block["type"] == "list":
            output += _list_block(block["data"])
        elif block["type"] == "quote":
            output += _quote_block(block["data"])
        elif block["type"] == "heading":
            output += _heading_block(block["data"])
        else:
            raise RuntimeError("Cannot render an unsupported sirtrevor block.")

    return output


def put_text_in_trevor(text):
    return json.dumps({"data": [{"type": "text", "data": {"text": text}}]})


def _text_block(data):
    return _render_markdown(data["text"]).replace("|", "<br />")


def _list_block(data):
    return _render_markdown(data["text"])


def _quote_block(data):
    unique_tag = "ThisIsAUniqueTag"
    # Append the tag before line breaks.
    text = data["text"].replace("\n", unique_tag + "\n")
    return _render_markdown(text).replace(unique_tag, "<br />")


def _heading_block(data):
    return "<h2>" + _render_markdown(data["text"]) + "</h2>"


def _render_markdown(text):
    html = markdown.markdown(text)
    return bleach.clean(html, tags=_BLEACH_ALLOWED_TAGS)


def trevor_to_md(trevor_data):
    parsed = json.loads(trevor_data)
    output = []

    for block in parsed["data"]:
        output.append(block["data"]["text"].strip())

    return "\n\n".join(output)
