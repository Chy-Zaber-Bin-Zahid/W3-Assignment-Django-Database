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
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'center', 'location_id', 'published', 'created_at', 'updated_at', 'user')
    list_filter = ('published', 'location_id') 
    search_fields = ('title', 'country_code', 'location__title')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """Limit queryset to show only accommodations created by the logged-in user for Property Owners."""
        query = super().get_queryset(request)
        if request.user.groups.filter(name='Property Owners').exists():
            # Show only the accommodations created by the logged-in user
            return query.filter(user=request.user)
        return query

    def get_form(self, request, obj=None, **kwargs):
        """Customize the form to automatically set and disable the user field."""
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['user'].disabled = True
        return form

    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(LocalizeAccommodation)
class LocalizeAccommodation(admin.ModelAdmin):
    list_display = ('id', 'accommodation', 'language', 'description')
    list_filter = ('language',)
    search_fields = ('description', 'language')