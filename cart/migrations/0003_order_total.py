# Generated by Django 5.0.1 on 2024-02-28 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_order_address_remove_order_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
