# Generated by Django 4.2.3 on 2023-08-11 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionbids',
            name='is_winner',
            field=models.BooleanField(default=False),
        ),
    ]
