from django.urls import path
from .views import LoginView, RegisterView, ProfileView, LogoutView, CreateListingView
from .views import ListingDetailView, UpdateListingView
app_name = "user"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create/", CreateListingView.as_view(), name="create_listing"),
    path("listing/<slug:slug>/", ListingDetailView.as_view(), name="listing_detail"),
    path("listing/<slug:slug>/edit/", UpdateListingView.as_view(), name="update_listing"),
]

