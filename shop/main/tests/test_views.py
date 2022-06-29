import pytest
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from django.test import TestCase, RequestFactory
from mixer.backend.django import mixer
from main import views
from main.models import Product, Category


@pytest.mark.django_db
class Test():
    @pytest.mark.parametrize('url_name, view_func, html_file',
                                 [('main', views.get_main_page, 'main/main.html'),
                                  ('about', views.get_about_us_page, 'main/about_us.html'),
                                  ('categories', views.get_categories, 'main/categories.html'),
                                  ('products', views.get_products_page, 'main/products.html'),
                                  ('registration', views.get_registration_page, 'main/registration.html'),
                                  ('login', views.get_login_page, 'main/login.html')])
    def test_simple(self, client, url_name, view_func, html_file):
        path = reverse(url_name)

        request = RequestFactory().get(path)
        SessionMiddleware().process_request(request)

        response = view_func(request)
        assert response.status_code == 200
        assertTemplateUsed(client.get(path), html_file)

    def test_with_slug(self):
        product_slug = 'Some_random_slug'

        product = mixer.blend('main.Product', title = product_slug, category = mixer.blend('main.Category'))
        product.save()
        path = reverse('specific_product_url_with_slug', kwargs={'slug': product_slug.lower()})

        request = RequestFactory().get(path)
        SessionMiddleware().process_request(request)
        response = views.get_specific_product(request, product_slug.lower())
        product.delete()
        assert response.status_code == 200


@pytest.fixture
def user_data():
    return {'username': 'random_username', 'password': 'random_password'}


@pytest.fixture
def create_user(user_data):
    user_model = get_user_model()

    user = user_model.objects.create_user(**user_data)
    user.set_password(user_data.get('password'))
    return user


@pytest.fixture
def create_authenticated_user(client, user_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    # test_user.save()
    client.login(**user_data)
    return test_user


@pytest.mark.django_db
class TestUserActions():
    def test_user_signup(self, client, user_data):
        user = get_user_model()
        assert user.objects.count() == 0

        path = reverse('registration')
        response = client.post(path, user_data)
        assert response.status_code == 302
        # assert user.objects.count() == 1

    def test_user_login(self, client, create_user, user_data):
        user = get_user_model()
        assert user.objects.count() == 1

        path = reverse('login')
        resp = client.post(path, data=user_data)
        assert resp.status_code == 302

    def test_user_logout(self, client, create_authenticated_user):
        path = reverse('logout_user')
        response = client.get(path)
        assert response.status_code == 302
