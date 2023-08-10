from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass # username 

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    starting_bid = models.FloatField()
    image_url = models.CharField(max_length=64,null=True)
    category = models.CharField(max_length=64,default="Toys")
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Title: {self.title} Price: {self.starting_bid} Description: {self.description}"

class AuctionBids(models.Model):
    auction = models.ForeignKey(AuctionListing,on_delete=models.CASCADE)
    price = models.FloatField()
    bidder = models.ForeignKey(User,on_delete=models.CASCADE)
    
class AuctionListingComments(models.Model):
    content = models.CharField(max_length=128)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)