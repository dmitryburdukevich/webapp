import pytest
from django.contrib.auth.models import AnonymousUser, User
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.urls import reverse
from django.test import TestCase, RequestFactory
from mixer.backend.django import mixer
from orders import views


@pytest.mark.django_db
class TestOrderCreate:
    def test_put_request(self, client):
        path = reverse('orders:order_create')
        view_func = views.order_create

        request = RequestFactory().get(path)
        SessionMiddleware().process_request(request)
        request.user = 1

        request.method = 'PUT'
        response = view_func(request)
        assert response.status_code == 200
        assertTemplateUsed(client.get(path), 'orders/create.html')

    def test_post_request(self, client):
        path = reverse('orders:order_create')
        view_func = views.order_create
        request = RequestFactory().post(path, {'first_name': 'name1', 'last_name': 'name2', 'email': 'email@gmail.com',
                                               'address': 'Nemiga', 'postal_code': '123456', 'city': 'Minsk'})
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)
        request.user = User.objects.create_user(username='the_username', password='password', email='lalala@gmail.com')
        print('reqPost:', request.POST)
        response = view_func(request)
        assert response.status_code == 200