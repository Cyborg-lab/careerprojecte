from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from listings.models import Listing, ListingImage

class CreateListingView(LoginRequiredMixin, View):
    login_url = "user:login"

    def get(self, request):
        return render(request, "create_listing.html")

    def post(self, request):
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        year = request.POST.get("year")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category = request.POST.get("category")
        image = request.FILES.get("image") 

        if not all([brand, model, year, price]):
            return render(request, "user/create_listing.html", {
                "error": "Iltimos, hamma majburiy maydonlarni to‘ldiring"
            })

       
        listing = Listing.objects.create(
            user=request.user,
            brand=brand,
            model=model,
            year=year,
            description=description,
            price=price,
            category=category
        )

       
        if image:
            ListingImage.objects.create(listing=listing, image=image)

        return redirect("index")
    
class UpdateListingView(LoginRequiredMixin, UpdateView):
    model = Listing
    template_name = "update.html"
    fields = ["description", "phone", "email"]
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return self.request.user.listings.all()


class ListingDetailView(DetailView):
    model = Listing
    template_name = "details.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing = self.get_object()
        context["images"] = listing.images.all()
        return context


class LoginView(View):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "user/login.html", {
                "error": "Username va password kiriting"
            })

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")

        return render(request, "user/login.html", {
            "error": "Username yoki password noto‘g‘ri"
        })


class RegisterView(View):
    def get(self, request):
        return render(request, "user/register.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not all([username, email, password]):
            return render(request, "user/register.html", {
                "error": "Hamma maydonni to‘ldiring"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "user/register.html", {
                "error": "Bu username band"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect("index")


class ProfileView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        listings = request.user.listings.all()
        return render(request, "user/profile.html", {"listings": listings})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")