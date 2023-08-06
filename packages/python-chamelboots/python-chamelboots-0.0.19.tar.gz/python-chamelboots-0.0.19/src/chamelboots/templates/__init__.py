"""Load templates."""

import itertools as it
import os
from pathlib import Path

from chameleon import PageTemplate
from lxml import etree

from .. import ChameleonTemplate
from .. import TalStatement
from ..constants import HTML_PARSER

# Create bootstrap starter template programatically from Bootstrap example.

BASEDIR = Path(os.path.abspath(__file__)).parent
BOOTSTRAP_TEMPLATES_DIR = BASEDIR.joinpath("bootstrap")
RAW_HTML_DIR = BOOTSTRAP_TEMPLATES_DIR.joinpath("raw_html")
BOOTSTRAP_START_TEMPLATE_HTML = RAW_HTML_DIR.joinpath("starter_template.html")
assert (
    BOOTSTRAP_START_TEMPLATE_HTML.exists()
), f"Missing file: {BOOTSTRAP_START_TEMPLATE_HTML}"
tree = etree.fromstring(BOOTSTRAP_START_TEMPLATE_HTML.read_text(), HTML_PARSER)

bootstrap_tag_classes = [
    (f"", e.tag, e.attrib) for e in tree.iterdescendants() if e.attrib
]


DOT = "."


# Copy and paste from Boostrap documentation for starter template.
HEAD_HTML = """  <head>
<!-- Required meta tags -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<!-- Bootstrap CSS -->
<link
rel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
crossorigin="anonymous">
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script
defer
src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
crossorigin="anonymous"></script>
<script
defer
src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
crossorigin="anonymous"></script>
<script
defer
src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
crossorigin="anonymous"></script>
<title>${title}</title>
</head>
"""
tree = etree.fromstring(HEAD_HTML, HTML_PARSER)
# lxml e.tag is not a string if it's a comment
HEAD_CHILD_TAGS, HEAD_CHILD_ATTRS = zip(
    *it.islice(
        ((e.tag, e.attrib) for e in tree.iterdescendants() if isinstance(e.tag, str)),
        1,
        None,
        None,
    )
)
assert all((HEAD_CHILD_TAGS, HEAD_CHILD_ATTRS)), "No child tags or attrs found."
CHANGING_KEYS = ("defer", "crossorigin", "src", "integrity", "href", "rel")

ATTRS = tuple({k: attr.get(k) for k in CHANGING_KEYS} for attr in HEAD_CHILD_ATTRS)
assert len(ATTRS) == len(HEAD_CHILD_TAGS)
changing_ = zip(HEAD_CHILD_TAGS, ATTRS)
MUTABLE_ATTRS = [
    {key: {k: v for k, v in d.items() if v is not None}}
    for key, d in changing_
    if any(d.values())
]
MUTABLE_TAGS = list(it.chain.from_iterable(item.keys() for item in MUTABLE_ATTRS))
START = HEAD_CHILD_TAGS.index("link")
IMMUTABLE_ATTRS = [*HEAD_CHILD_ATTRS[:START], *HEAD_CHILD_ATTRS[-1:]]
IMMUTABLE_TAGS = [*HEAD_CHILD_TAGS[:START], *HEAD_CHILD_TAGS[-1:]]
immutable_data = [{key: value} for key, value in zip(IMMUTABLE_TAGS, IMMUTABLE_ATTRS)]
mutable_data = MUTABLE_ATTRS


def write_boostrap_starter_template(directory: Path):
    """Create a template from scratch given only the MUTABLE_ATTRS.
    Must be in same order as HEAD_CHILD_TAGS."""

    def data_key(item):
        """Use to sort tags into appropriate order."""
        (key,) = item.keys()
        return HEAD_CHILD_TAGS.index(key)

    head_children = [
        ChameleonTemplate(
            tag=tag, tal_statements=(TalStatement("attributes", "attrib"),)
        ).render(attrib=attrib)
        for data in sorted((*immutable_data, *mutable_data), key=data_key)
        for tag, attrib in data.items()
    ][
        :-1
    ]  # remove title
    # structure Chameleon statement  keeps the HTML intact. It is not encoded.
    head = ChameleonTemplate(
        tag="head",
        tal_statements=(TalStatement("content", "structure inner"),),
        inner_content="",
    )

    title = etree.Element("title")
    title.text = "${title}"
    title = etree.tostring(title, method="html").decode()
    # add title inside of head
    # render a head, splitlines for readability
    head_html = head.render(inner="\n".join([*head_children, title]))
    # Is it valid HTML?
    assert etree.fromstring(head_html, HTML_PARSER)
    # Write the bootstrap starter template to file.
    seed_template = Path(os.path.abspath(__file__)).parent.joinpath(
        "seed", "index.html"
    )
    directory.joinpath("index.tmpl.html").write_text(
        PageTemplate(seed_template.read_text()).render(
            head=head_html,
            body_template_tag='<div tal:omit-tag tal:content="structure body_content"></div>',
        )
    )
    return directory
