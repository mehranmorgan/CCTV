# Generated by Django 5.0.1 on 2024-05-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_order_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
