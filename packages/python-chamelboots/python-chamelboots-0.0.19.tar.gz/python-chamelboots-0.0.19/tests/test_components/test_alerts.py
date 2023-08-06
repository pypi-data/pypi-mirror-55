#!/usr/bin/env python
# coding: utf-8

# In[1]:


import lxml.etree

from chamelboots.bootstrap.components.alerts import ALERT_COMPONENTS
from chamelboots.bootstrap.components.constants import ALERT_CLASSES_ATTRIBS
from chamelboots.bootstrap.components.constants import ContextualClassNames
from chamelboots.constants import FAKE
from chamelboots.constants import HTML_PARSER

# In[2]:


# In[3]:


# In[4]:


def test_alerts():
    """Test creation of Bootstrap alert components."""

    expected = {tuple(d.values()) for d in ALERT_CLASSES_ATTRIBS.values()}

    for key, alert_component in ALERT_COMPONENTS.items():
        html_string = alert_component(inner_content=FAKE.paragraph()).html_string
        tree = lxml.etree.fromstring(html_string, HTML_PARSER)
        (values,) = [
            tuple(element.attrib.values())
            for element in tree.iterdescendants()
            if element.attrib
        ]
        assert values in expected
        contextual_class, _ = (
            [
                contextual_class_name in value
                for contextual_class_name in ContextualClassNames
            ]
            for value in values
        )
        assert any(contextual_class)


# In[5]:


if __name__ == "__main__":
    import pytest
    import shlex

    pytest.main(shlex.split("-xs test_alerts.py"))
