from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

from django.urls import reverse
from django.utils.text import slugify
from django.contrib import messages
import datetime
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    email_is_verified = models.BooleanField(default=False)

    def get_full_name(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def __str__(self):
        return self.user.username + '_profile'


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="title")
    image = models.ImageField(verbose_name="Image", default="default.jpg")
    slug = models.SlugField(default='', editable=False, max_length=50, unique=True)

    @property
    def get_valid_url_for_products(self):
        return reverse('products') + '?category=' + str(self.slug)

    def save(self, *args, **kwargs):
        from django.template import defaultfilters
        from unidecode import unidecode

        value = self.title
        self.slug = defaultfilters.slugify(unidecode(value),)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


def validate_amount_of_product(value):
    max_value = 1000
    if value > max_value:
        raise ValidationError(f'Amount could not be bigger than {max_value}')
    else:
        return value


class ProductReward(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag


class Product(models.Model):
    title = models.CharField('Name', max_length=50)
    description = models.TextField('Description', max_length=255, default="Some description ...")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=99.99)
    amount = models.PositiveIntegerField(default=5, validators=[validate_amount_of_product])
    image = models.ImageField(verbose_name="Image", default="default_img.jpg")
    slug = models.SlugField(default='', editable=False, max_length=50, unique=True)
    rewards = models.ManyToManyField(ProductReward, default='No awards')

    @property
    def get_string_price(self):
        return str(self.price) + '$'

    def get_absolute_url(self):
        return reverse('specific_product_url_with_slug', args=(self.slug,))

    def save(self, *args, **kwargs):
        from django.template import defaultfilters
        from unidecode import unidecode

        self.slug = defaultfilters.slugify(unidecode(self.title),)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


