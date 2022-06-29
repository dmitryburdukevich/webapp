from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Category, Product, Profile


class TestCategoryModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(title='Cars', pk=1)

    def test_title_label(self):
        category = Category.objects.get(pk=1)
        field_label = category._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_slug_label(self):
        category = Category.objects.get(pk=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_image_label(self):
        category = Category.objects.get(pk=1)
        field_label = category._meta.get_field('image').verbose_name
        self.assertEquals(field_label, "Image")

    def test_title_max_length(self):
        category = Category.objects.get(pk=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEquals(max_length, 50)

    def test_slug_max_length(self):
        category = Category.objects.get(pk=1)
        max_length = category._meta.get_field('slug').max_length
        self.assertEquals(max_length, 50)


class TestProductModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Product.objects.create(title='Computer_1', category=Category.objects.create(title='Computers'))

    def test_title_label(self):
        product = Product.objects.get(pk=1)
        field_label = product._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Name')

    def test_description_label(self):
        product = Product.objects.get(pk=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Description')

    def test_price_max_digits(self):
        product = Product.objects.get(pk=1)
        max_digits = product._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 9)

    def test_image_label(self):
        product = Product.objects.get(pk=1)
        field_label = product._meta.get_field('image').verbose_name
        self.assertEquals(field_label, "Image")

    def test_slug_max_length(self):
        product = Product.objects.get(pk=1)
        max_length = product._meta.get_field('slug').max_length
        self.assertEquals(max_length, 50)


class TestProfileModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='Misha')

    def test_phone_number_max_length(self):
        profile = Profile.objects.get(user=User.objects.get(pk=1))
        max_length = profile._meta.get_field('phone_number').max_length
        self.assertEquals(max_length, 12)

    def test_address_max_length(self):
        profile = Profile.objects.get(user=User.objects.get(pk=1))
        max_length = profile._meta.get_field('address').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_username_and_profile(self):
        profile = Profile.objects.get(user=User.objects.get(pk=1))
        expected_object_name = profile.user.username + '_profile'
        self.assertEquals(expected_object_name, str(profile))