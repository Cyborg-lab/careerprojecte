from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Listing(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold")
    ]
    CATEGORY_CHOICES = [
        ("sedan", "Sedan"),
        ("suv", "SUV"),
        ("hatchback", "Hatchback"),
        ("pickup", "Pickup Truck"),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    slug = models.SlugField(unique=True, blank=True)

    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand}-{self.model}-{self.year}")
            slug = base_slug
            counter = 1
            while Listing.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def main_image(self):
        img = self.images.first()
        return img.image.url if img else None

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cars/")

    def __str__(self):
        return f"Image for {self.listing.brand} {self.listing.model}"