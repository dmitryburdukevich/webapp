from mixer.backend.django import mixer
from django.urls import reverse
from orders import models
import pytest


@pytest.mark.django_db
class TestModels:
    def test_order(self):
        assert models.Product.objects.count() == 0
        order = mixer.blend('orders.Order')
        assert order.id == 1
        assert order.__str__() == 'Order 1'

    def test_order_item(self):
        assert models.Product.objects.count() == 0
        order_item = models.OrderItem.objects.create(order=mixer.blend('orders.Order'),
                                                     product=mixer.blend('main.Product',
                                                                         category=mixer.blend('main.Category')),
                                                     price=123, quantity=10)
        assert order_item.id == 1
        assert order_item.__str__() == '1'
        assert order_item.get_cost() == 1230