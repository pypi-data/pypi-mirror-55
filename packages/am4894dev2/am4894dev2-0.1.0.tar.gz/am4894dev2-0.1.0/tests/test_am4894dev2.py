#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `am4894dev2` package."""

import pytest


from am4894dev2 import am4894dev2


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_hello():
    res = am4894dev2.hello('test')
    assert res == 'test'
