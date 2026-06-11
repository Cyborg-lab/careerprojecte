
from django.shortcuts import render
from listings.models import Listing
from .models import Listing

def index(request):

    listings = Listing.objects.all().order_by("-created_at")

    return render(request, "index.html", {
        "listings": listings
    })



