import pytest


def test_baseclass():
    """Improve coverage."""

    from chamelboots.bootstrap.components import _Component

    with pytest.raises(TypeError):
        _Component(attrib=None, template=None)
