import pytest
from django.urls import reverse, resolve


@pytest.mark.parametrize('url_name', ['orders:order_create', 'orders:order_all'])
def test_simple(url_name):
    path = reverse(url_name)
    assert resolve(path).view_name == url_name


def test_order_specific():
    url_name = 'orders:order_specific'
    path = reverse(url_name, args='1')
    assert resolve(path).view_name == url_name