from django.contrib import admin
from .models import User, AuctionBids, AuctionListing,AuctionListingComments
# Register your models here.

class AuctionAdminForm(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user  # Ustaw właściciela aukcji na aktualnie zalogowanego użytkownika
        super().save_model(request, obj, form, change)

admin.site.register(User)
admin.site.register(AuctionBids)
admin.site.register(AuctionListingComments)
admin.site.register(AuctionListing, AuctionAdminForm)
