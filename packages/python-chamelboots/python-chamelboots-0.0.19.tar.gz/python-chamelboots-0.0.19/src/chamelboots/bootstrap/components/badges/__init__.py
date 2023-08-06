"""Create Bootstrap badges."""

from lxml import etree

from ....constants import HTML_PARSER
from ...components.constants import ContextualClassNames
from .. import _Component

# from Boostrap documentation
BADGES_HTML = """<span class="badge badge-primary">Primary</span>
<span class="badge badge-secondary">Secondary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-danger">Danger</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-info">Info</span>
<span class="badge badge-light">Light</span>
<span class="badge badge-dark">Dark</span>"""

tree = etree.fromstring(BADGES_HTML, HTML_PARSER)

BADGES = tuple(e.attrib for e in tree.iter() if e.attrib)
NAMES = tuple(f"{name.value.title()}Badge" for name in ContextualClassNames)
TEMPLATES = SPAN_TEMPLATE, LINK_TEMPLATE = (
    '<span tal:attributes="attrib">${inner_content}</span>',
    '<a tal:attributes="attrib">${inner_content}</a>',
)


def create_badge_components(template) -> dict:

    return dict(
        zip(
            NAMES,
            (
                type(name, (dict, _Component,), dict(template=template, attrib=attrib))
                for name, attrib in zip(NAMES, BADGES)
            ),
        )
    )


SPAN_BADGE_COMPONENTS, LINK_BADGE_COMPONENTS = (
    create_badge_components(template) for template in TEMPLATES
)
