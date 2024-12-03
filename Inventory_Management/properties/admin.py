from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, LocalizeAccommodation

@admin.register(Location)
class Location(LeafletGeoAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')


@admin.register(Accommodation)
class Accommodation(LeafletGeoAdmin):
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'center', 'location_id', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'location_id') 
    search_fields = ('title', 'country_code', 'location__title')
    ordering = ('-created_at',)


@admin.register(LocalizeAccommodation)
class LocalizeAccommodation(admin.ModelAdmin):
    list_display = ('id', 'accommodation', 'language', 'description')
    list_filter = ('language',)
    search_fields = ('description', 'language')