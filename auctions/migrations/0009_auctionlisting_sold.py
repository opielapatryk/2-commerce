# Generated by Django 4.2.3 on 2023-08-11 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionbids_is_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]
