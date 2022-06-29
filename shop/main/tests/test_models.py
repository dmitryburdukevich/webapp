from mixer.backend.django import mixer
from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestModels:
    def test_product(self):
        product = mixer.blend('main.Product', title='the_title', price=10,
                              category = mixer.blend('main.Category'))
        assert product.title == product.__str__()
        assert product.title == 'the_title'
        assert product.get_string_price == '10$'

    def test_category(self):
        title = 'random_title'
        category = mixer.blend('main.Category', title=title)
        assert category.get_valid_url_for_products == reverse('products') + f'?category={title}'
        assert category.__str__() == title
