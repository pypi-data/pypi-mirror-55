"""Define constants used in Boostrap."""
import itertools as it
from enum import Enum

from lxml import etree

from ... import ChameleonTemplate
from ... import TalStatement
from ...constants import HTML_PARSER

CLASS = "class"
# Taken from Bootstrap docs.
ALERTS_HTML = """<div class="alert alert-primary" role="alert">
  A simple primary alert—check it out!
</div>
<div class="alert alert-secondary" role="alert">
  A simple secondary alert—check it out!
</div>
<div class="alert alert-success" role="alert">
  A simple success alert—check it out!
</div>
<div class="alert alert-danger" role="alert">
  A simple danger alert—check it out!
</div>
<div class="alert alert-warning" role="alert">
  A simple warning alert—check it out!
</div>
<div class="alert alert-info" role="alert">
  A simple info alert—check it out!
</div>
<div class="alert alert-light" role="alert">
  A simple light alert—check it out!
</div>
<div class="alert alert-dark" role="alert">
  A simple dark alert—check it out!
</div>"""

tree = etree.fromstring(ALERTS_HTML, HTML_PARSER)
_alert_classes_attribs_values, __alert_classes_attribs_values = it.tee(
    e.attrib for e in tree.iterdescendants() if e.attrib
)

_contextual_class_names = [
    item[CLASS].split()[-1].split("-")[-1] for item in __alert_classes_attribs_values
]
ContextualClassNames = Enum(
    "ContextualClassNames",
    type=str,
    names=zip(
        (item.upper() for item in _contextual_class_names), _contextual_class_names
    ),
)
ALERT_CLASSES_ATTRIBS = dict(zip(ContextualClassNames, _alert_classes_attribs_values))
COMPONENT_CLASS_NAMES = [
    "".join(word.title() for word in value[CLASS].split()[-1].split("-"))
    for value in ALERT_CLASSES_ATTRIBS.values()
]
ATTRIBUTE_LOOKUP = dict(zip(COMPONENT_CLASS_NAMES, ALERT_CLASSES_ATTRIBS.values()))
DIV_TEMPLATE_STRING = """<div tal:attributes="attrib">
  ${inner_content}
</div>"""
DIV_TEMPLATE_STRING = ChameleonTemplate(
    tal_statements=(TalStatement("attributes", "attrib"),),
    inner_content="${inner_content}",
).html_string
