# Generated by Django 4.1.5 on 2023-04-16 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0024_alter_delivery_options_alter_delivery_delivered_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payments',
            options={'ordering': ['-payed_at', 'ref']},
        ),
    ]
