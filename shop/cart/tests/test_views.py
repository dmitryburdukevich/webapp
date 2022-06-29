import pytest
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from django.test import TestCase, RequestFactory
from cart import views
from mixer.backend.django import mixer


@pytest.mark.django_db
class Test():
    def test_cart_detail_view(self, client):
        path = reverse('cart:cart_detail')

        request = RequestFactory().get(path)
        SessionMiddleware().process_request(request)

        response = views.cart_detail(request)
        assert response.status_code == 200
        assertTemplateUsed(client.get(path), 'cart/cart.html')

    @pytest.mark.parametrize('url_name, view_func',
                             [('cart:cart_add', views.cart_add),
                              ('cart:cart_remove', views.cart_remove)])
    def test_cart_actions_view(self, url_name, view_func):
        path = reverse(url_name, kwargs={'product_id': 1})
        mixer.blend('main.Product', id=1, category=mixer.blend('main.Category'))

        request = RequestFactory().get(path)
        SessionMiddleware().process_request(request)

        response = view_func(request, 1)
        if url_name == 'cart:cart_add':
            assert response.status_code == 405
        else:
            assert response.status_code == 302
