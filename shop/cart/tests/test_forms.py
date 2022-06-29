from django.test import TestCase
from cart.forms import CartAddProductForm


class TestCartAddProductForm(TestCase):
    def test_quantity_coerce_int(self):
        form = CartAddProductForm()
        self.assertTrue(form.fields['quantity'].coerce == int)

    def test_update_quantity_required_false(self):
        form = CartAddProductForm()
        self.assertTrue(form.fields['update_quantity'].required == False)

    def test_update_quantity_initial(self):
        form = CartAddProductForm()
        self.assertTrue(form.fields['update_quantity'].initial == True)