# Generated by Django 3.1.7 on 2021-06-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210606_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default_img.jpg', upload_to='', verbose_name='Image'),
        ),
    ]
