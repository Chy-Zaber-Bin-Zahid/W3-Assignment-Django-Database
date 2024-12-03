from django.db import models
from django.contrib.gis.db import models as geomodels  # For spatial fields
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # Unique ID
    title = models.CharField(max_length=100)  # Location title
    center = geomodels.PointField()  # Geospatial PointField for location center
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )  # Self-referential foreign key for hierarchical structure
    location_type = models.CharField(
        max_length=20,
        choices=[('country', 'Country'), ('state', 'State'), ('city', 'City')],
        default='city'
    )  # Location type (country, state, city)
    country_code = models.CharField(max_length=2)  # ISO country code
    state_abbr = models.CharField(max_length=3, null=True, blank=True)  # State abbreviation
    city = models.CharField(max_length=30, null=True, blank=True)  # City name
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp


    def __str__(self):
        return f"{self.title} ({self.location_type})"
    

class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # String ID with max length of 20
    feed = models.PositiveSmallIntegerField(default=0)  # Feed number, unsigned small integer
    title = models.CharField(max_length=100)  # Name of the accommodation
    country_code = models.CharField(max_length=2)  # ISO country code
    bedroom_count = models.PositiveIntegerField()  # Number of bedrooms
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)  # Review score (1 decimal place)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Price rate in USD
    center = geomodels.PointField()  # Geolocation field
    # images = models.JSONField(null=True, blank=True)  # Array of image URLs
    images = models.JSONField(
        null=True, 
        blank=True,
    )
    location = models.ForeignKey('properties.Location', on_delete=models.CASCADE, related_name="accommodations")  # ForeignKey to Location

    # JSONB Array of Amenities
    amenities = models.JSONField(
        null=True, 
        blank=True,
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # ForeignKey to Django's auth_user
    published = models.BooleanField(default=False)  # Boolean to indicate if the accommodation is published
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last update timestamp


    def __str__(self):
        return f"{self.title} - {self.location.title}"
    

class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE, related_name='localized')
    language = models.CharField(max_length=2)  # Language code (ISO 639-1, e.g., 'en', 'ar')
    description = models.TextField()  # Localized description
    policy = models.JSONField(null=True, blank=True)  # JSON field for policies


    def __str__(self):
        return f"{self.accommodation.title} ({self.language})"