from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, AuctionBids, AuctionListing,AuctionListingComments,Watchlist
from django import forms


def index(request):
    active_auctions = AuctionListing.objects.filter(sold=False)
    return render(request, "auctions/index.html",{
        'auctions': active_auctions,
    })

class CreateBidForm(forms.Form):
    new_bid = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '99.99',}))

class CreateCommentForm(forms.Form):
     new_comment = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'placeholder': 'Comment'}))

def listing(request,listing_id):
    if request.user.is_authenticated:
        try:

            watchlist_entry = Watchlist.objects.get(owner=request.user, auction=AuctionListing.objects.get(id=listing_id))
            submit = 'Delete From Watchlist'
            if 'watchlist' in request.POST:
                watchlist_entry.delete()
                submit = 'Add To Watchlist'
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            
            elif 'close' in request.POST:
                auction_listing = AuctionListing.objects.get(id=listing_id)
                bids = AuctionBids.objects.filter(auction=auction_listing)
                if bids.exists():
                        last_bid = bids.last()
                        last_bid.is_winner = True
                        last_bid.save()

                        auction_listing.sold = True
                        auction_listing.save()
                        
                        if request.user == last_bid.bidder:
                            message = 'You have won the auction'
                            return render(request, "auctions/listing.html",{
                                'auction': AuctionListing.objects.get(id=listing_id),
                                'submit':submit,
                                'form': CreateBidForm(),
                                'commentInput': CreateCommentForm(),
                                'message': message
                            })

            elif 'bid' in request.POST:

                form = CreateBidForm(request.POST)
                if form.is_valid():
                    # define auction
                    auction_listing = AuctionListing.objects.get(id=listing_id)

                    # define new bid price
                    new_bid = form.cleaned_data['new_bid']

                    """ before save
                        check if new bid is at least same as starting_bid
                    """

                    if new_bid >= auction_listing.starting_bid:
                        # define auction bid
                        auction_bid = AuctionBids(auction=auction_listing, price=new_bid, bidder=request.user)
                        # save auction bid
                        auction_bid.save()

                        # set new auction price
                        auction_listing.starting_bid = new_bid

                        # save new auction price
                        auction_listing.save()

                    else:
                        return render(request, "auctions/listing.html",{
                            'auction': AuctionListing.objects.get(id=listing_id),
                            'submit':submit,
                            'form': CreateBidForm(),
                            'commentInput': CreateCommentForm(),

                            'message': "Too small bid.."
                        })
                    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            elif 'comment' in request.POST:
                form = CreateCommentForm(request.POST)
                if form.is_valid():
                    auction_listing = AuctionListing.objects.get(id=listing_id)

                    comment = AuctionListingComments(content=form.cleaned_data['new_comment'],auction=auction_listing,creator=request.user)
                    comment.save()

        except Watchlist.DoesNotExist:
                submit = 'Add To Watchlist'
                watchlist = Watchlist(owner=request.user,auction=AuctionListing.objects.get(id=listing_id))
                submit = 'Add To Watchlist'
                if 'watchlist' in request.POST:
                    watchlist.save()
                    submit = 'Delete From Watchlist'
                    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                elif 'close' in request.POST:
                    auction_listing = AuctionListing.objects.get(id=listing_id)
                    bids = AuctionBids.objects.filter(auction=auction_listing)
                    if bids.exists():
                        last_bid = bids.last()
                        last_bid.is_winner = True
                        last_bid.save()

                        auction_listing.sold = True
                        auction_listing.save()
                        if request.user == last_bid.bidder:
                                                    message = 'You have won the auction'
                                                    return render(request, "auctions/listing.html",{
                                    'auction': AuctionListing.objects.get(id=listing_id),
                                    'submit':submit,
                                    'form': CreateBidForm(),
                                    'commentInput': CreateCommentForm(),

                                    'message': message
                                })

                elif 'bid' in request.POST:
                    form = CreateBidForm(request.POST)
                    if form.is_valid():
                        # define auction
                        auction_listing = AuctionListing.objects.get(id=listing_id)

                        # define new bid price
                        new_bid = form.cleaned_data['new_bid']

                        """ before save
                            check if new bid is at least same as starting_bid
                        """

                        if new_bid >= auction_listing.starting_bid:
                            # define auction bid
                            auction_bid = AuctionBids(auction=auction_listing, price=new_bid, bidder=request.user)
                            # save auction bid
                            auction_bid.save()
                            # set new auction price
                            auction_listing.starting_bid = new_bid

                            # save new auction price
                            auction_listing.save()             
                        else:
                            return render(request, "auctions/listing.html",{
                                
                                'auction': AuctionListing.objects.get(id=listing_id),
                                'submit':submit,
                                'form': CreateBidForm(),
                                'commentInput': CreateCommentForm(),

                                'message': "Too small bid.."
                            })
                        


                        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                elif 'comment' in request.POST:
                    form = CreateCommentForm(request.POST)
                    if form.is_valid():
                        auction_listing = AuctionListing.objects.get(id=listing_id)

                        comment = AuctionListingComments(content=form.cleaned_data['new_comment'],auction=auction_listing,creator=request.user)
                        comment.save()
        auction_listing = AuctionListing.objects.get(id=listing_id)
        return render(request, "auctions/listing.html",{
            'auction': auction_listing,
            'submit':submit,
            'form': CreateBidForm(),
            'commentInput': CreateCommentForm(),
            'comments': AuctionListingComments.objects.filter(auction=auction_listing),
        })
    auction_listing = AuctionListing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html",{
        'auction': auction_listing,
        'comments': AuctionListingComments.objects.filter(auction=auction_listing),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class CreateNewListingForm(forms.Form):
    title = forms.CharField(max_length=64,widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    desc = forms.CharField(max_length=128,widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    starting_bid = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '99.99'}))
    image_url = forms.CharField(max_length=64,empty_value=True,widget=forms.TextInput(attrs={'placeholder': 'path/img'}))
    category = forms.CharField(max_length=64,widget=forms.TextInput(attrs={'placeholder': 'Category'}))

def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.method == 'POST':
            form = CreateNewListingForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                starting_bid = form.cleaned_data['starting_bid']
                image_url = form.cleaned_data['image_url']
                category = form.cleaned_data['category']
                creator = request.user
                auction = AuctionListing(title=title, description=desc, starting_bid=starting_bid, image_url=image_url, category=category, creator=creator)
                auction.save()
                return render(request, 'auctions/index.html')
        else:
            return render(request, "auctions/create.html",{
                "form": CreateNewListingForm()
            })
        
def watchlist(request):
     return render(request, "auctions/watchlist.html",{
          "watchlist": Watchlist.objects.filter(owner=request.user)
     })

def categories(request):
     return render(request, "auctions/categories.html",{
          "auctions": AuctionListing.objects.all()
     })

def category(request,category):
     return render(request, "auctions/category.html",{
          #all auctions with category == category
          'auctions': AuctionListing.objects.filter(category=category)
     })