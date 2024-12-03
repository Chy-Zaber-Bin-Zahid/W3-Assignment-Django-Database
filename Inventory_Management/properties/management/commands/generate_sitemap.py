import json
from django.core.management.base import BaseCommand
from properties.models import Location  # Replace with your actual model

class Command(BaseCommand):
    help = 'Generate sitemap.json for all country locations'

    def handle(self, *args, **kwargs):
        # Fetch all locations, order by location title alphabetically
        locations = Location.objects.all().order_by('title')

        # Organize locations by country
        sitemap_data = {}

        for location in locations:
            country_code = location.country_code.lower()
            country_name = location.country_code.upper()

            # Ensure country exists in the sitemap structure
            if country_name not in sitemap_data:
                sitemap_data[country_name] = {"slug": country_code, "locations": []}

            # Add the location to the corresponding country
            location_entry = {location.title: f"{country_code}/{location.title.lower()}"}
            sitemap_data[country_name]["locations"].append(location_entry)

        # Convert to the desired JSON structure
        sitemap_list = [
            {"country": country, "slug": data["slug"], "locations": data["locations"]}
            for country, data in sitemap_data.items()
        ]

        # Write the JSON data to a file
        with open('sitemap.json', 'w') as json_file:
            json.dump(sitemap_list, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.json'))
