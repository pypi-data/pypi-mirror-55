#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %load test_templates.py
import os
from pathlib import Path

import pytest
from chameleon import PageTemplateLoader
from lxml import etree

from chamelboots import ChameleonTemplate
from chamelboots import TalStatement
from chamelboots.bootstrap.components.badges import SPAN_BADGE_COMPONENTS
from chamelboots.constants import FAKE
from chamelboots.constants import HTML_PARSER
from chamelboots.templates import write_boostrap_starter_template

RAISES_VALUE_ERROR = pytest.raises(ValueError)


# In[2]:


def test_get_attr_proxy():
    """Use instance of ChameleonTemplate as inner value."""
    element = ChameleonTemplate()
    with pytest.raises(AttributeError):
        element.foo


# In[3]:


def test_tal_collection():
    """Use multiple tals to improve coverage."""
    # "<p tal:condition="request.message" tal:content="request.message" />"
    request = type("Request", (), {"message": "foo world"})()
    tal_statements = [
        TalStatement(name, value)
        for name, value in zip(("condition", "content"), ("request.message",) * 2)
    ]
    print(
        etree.tostring(
            etree.fromstring(
                ChameleonTemplate(tag="p", tal_statements=tal_statements).render(
                    request=request
                ),
                HTML_PARSER,
            ),
            method="html",
        )
    )
    request = type("Request", (), {"message": False})()
    assert not ChameleonTemplate(tag="p", tal_statements=tal_statements).render(
        request=request
    )


# In[4]:


@pytest.mark.parametrize(
    "args,expectation",
    [
        (("repeat", "${repeat}"), RAISES_VALUE_ERROR),
        (("foo", "foo foo"), RAISES_VALUE_ERROR),
        (("foo", "repeat foo"), RAISES_VALUE_ERROR),
    ],
)
def test_no_tal_keywords(args, expectation):
    """Test that error is thrown if context_value or inner_content has a tal keyword in it or the tal is not valid."""
    with expectation:
        kwargs = dict(tal_statements=TalStatement(*args))
        ChameleonTemplate(**kwargs)


# In[5]:


def test_html_doc_generation_with_badges(tmpdir):
    """Generate HTML documents."""

    badges = "\n".join(
        component(inner_content=FAKE.catch_phrase()).html_string
        for component in SPAN_BADGE_COMPONENTS.values()
    )

    # create starter template folder
    chameleon_templates_dir = tmpdir
    html_templates = PageTemplateLoader(chameleon_templates_dir.strpath)
    chameleon_templates_dir = write_boostrap_starter_template(
        Path(chameleon_templates_dir.strpath)
    )
    assert len(list(chameleon_templates_dir.iterdir())) == 1
    html = html_templates["index.tmpl.html"].render(
        body_content=badges, title=FAKE.name()
    )

    www = Path(os.path.abspath(__file__)).parent.parent.parent.joinpath("www")
    www.mkdir(exist_ok=True)

    www.joinpath("index.html").write_text(html)


# In[6]:


if __name__ == "__main__":
    import pytest
    import shlex

    pytest.main(shlex.split("-xs test_templates.py"))
