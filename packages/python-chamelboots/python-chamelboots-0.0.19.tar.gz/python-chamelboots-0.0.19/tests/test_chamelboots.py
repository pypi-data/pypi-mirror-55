#!/usr/bin/env python
# coding: utf-8

# In[1]:


from chamelboots.cli import main


def test_main():
    assert main([]) == 0


# In[3]:


if __name__ == "__main__":
    import pytest
    import shlex

    pytest.main(shlex.split("-xs test_chamelboots.py"))
