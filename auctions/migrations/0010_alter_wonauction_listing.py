# Generated by Django 5.0.2 on 2024-03-12 22:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wonauction',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
