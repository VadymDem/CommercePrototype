# Generated by Django 5.0.2 on 2024-03-12 22:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_wonauction_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wonauction',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
