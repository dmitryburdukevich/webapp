import pytest
from django.urls import reverse, resolve


@pytest.mark.parametrize('url_name', ['main', 'about', 'products', 'categories', 'registration', 'login',
                                      'logout_user', 'profile'])
def test_simple(url_name):
    path = reverse(url_name)
    assert resolve(path).view_name == url_name


def test_products_with_slug():
    url_name = 'specific_product_url_with_slug'
    path = reverse(url_name, kwargs={'slug': 'Some_random_slug'})
    assert resolve(path).view_name == url_name
