# Generated by Django 5.0.1 on 2024-03-08 19:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_alter_comericalslider_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comericalslider',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slider', to='Product.maincategory'),
        ),
    ]
