# Generated by Django 4.1.3 on 2022-12-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0002_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
    ]
