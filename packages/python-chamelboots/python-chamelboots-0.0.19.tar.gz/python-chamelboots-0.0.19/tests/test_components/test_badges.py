from lxml import etree

from chamelboots.bootstrap.components import badges
from chamelboots.bootstrap.components.badges import LINK_BADGE_COMPONENTS
from chamelboots.bootstrap.components.badges import SPAN_BADGE_COMPONENTS
from chamelboots.bootstrap.components.constants import CLASS
from chamelboots.bootstrap.components.constants import ContextualClassNames
from chamelboots.constants import FAKE
from chamelboots.constants import HTML_PARSER


def test_badges():
    """Test creation of badges."""

    assert all(
        (name in badge[CLASS])
        for badge, name in zip(badges.BADGES, ContextualClassNames)
    )
    for components in (
        SPAN_BADGE_COMPONENTS,
        LINK_BADGE_COMPONENTS,
    ):
        for key, value in components.items():
            tree = etree.fromstring(value.template, HTML_PARSER)
            _, _, element = tree.iter()
            component = value(inner_content=FAKE.catch_phrase())
            assert element.tag in component.html_string
