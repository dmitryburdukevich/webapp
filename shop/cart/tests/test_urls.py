import pytest
from django.urls import reverse, resolve
from cart import views


def test_simple():
    url_name = 'cart:cart_detail'
    path = reverse(url_name)
    assert resolve(path).view_name == url_name


@pytest.mark.parametrize('url_name', ['cart:cart_add', 'cart:cart_remove'])
def test_order_specific(url_name):
    path = reverse(url_name, args='1')
    assert resolve(path).view_name == url_name
