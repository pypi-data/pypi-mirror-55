"""Define an abstract base clase."""

from abc import ABC

from chameleon import PageTemplate

from ...constants import Join


class _Component(ABC):
    """Use Chameleon templates to replace only the attributes and inner
    content of Bootstrap components that change."""

    template = ""
    attrib = dict(foo="bar")

    def __init__(self, **kwargs):
        """Set :self.__dict__: to self when dict is extended.
        This allows spreading :self: into Chameleon templates as context."""
        required_attrs = (
            "template",
            "attrib",
        )
        if not all(attr in kwargs for attr in required_attrs):
            raise ValueError(
                f"'{Join.COMMASPACE(required_attrs)}' are all required kwargs."
            )
        super().__init__(**kwargs)
        self.__dict__ = self

    @property
    def html_string(self):
        """Create a Chameleon template from :self.template:.
        Spread :self: and :self.attrib: into render method on Chameleon template."""
        return PageTemplate(self.template).render(**{"attrib": self.attrib, **self})
