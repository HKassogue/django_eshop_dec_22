# Generated by Django 4.1.5 on 2023-04-16 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0022_alter_alerts_created_at_alter_arrival_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arrival_details',
            options={'verbose_name': 'Arrival details', 'verbose_name_plural': 'Arrivals details'},
        ),
        migrations.AlterModelOptions(
            name='coupon',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='coupon_type',
            options={'verbose_name_plural': 'coupons types'},
        ),
        migrations.AlterModelOptions(
            name='delivery',
            options={'ordering': ['-delivered_at', '-state']},
        ),
        migrations.AlterModelOptions(
            name='like',
            options={'ordering': ['-created_at', '-liked']},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at', 'reference']},
        ),
        migrations.AlterModelOptions(
            name='order_details',
            options={'verbose_name': 'Order details', 'verbose_name_plural': 'Orders details'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at', '-rate']},
        ),
        migrations.AddField(
            model_name='delivery',
            name='delivered_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
