import pytest
from django.contrib.gis.geos import Point
from properties.models import Location, Accommodation, LocalizeAccommodation
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


@pytest.mark.django_db
class TestLocationModel:
    def test_create_location(self):
        location = Location.objects.create(
            id="loc1",
            title="Dhaka",
            center=Point(90.4125, 23.8103),
            location_type="city",
            country_code="BD"
        )
        assert location.id == "loc1"
        assert location.title == "Dhaka"
        assert location.center.x == 90.4125
        assert location.center.y == 23.8103
        assert location.location_type == "city"
        assert location.country_code == "BD"


    def test_location_hierarchy(self):
        parent = Location.objects.create(
            id="country1",
            title="Bangladesh",
            center=Point(90.0, 23.0),
            location_type="country",
            country_code="BD"
        )
        child = Location.objects.create(
            id="city1",
            title="Dhaka",
            center=Point(90.4125, 23.8103),
            location_type="city",
            country_code="BD",
            parent=parent
        )
        assert child.parent == parent
        assert parent.children.count() == 1
        assert parent.children.first().title == "Dhaka"


@pytest.mark.django_db
class TestAccommodationModel:
    def test_create_accommodation(self):
        location = Location.objects.create(
            id="loc1",
            title="Dhaka",
            center=Point(90.4125, 23.8103),
            location_type="city",
            country_code="BD"
        )
        user = User.objects.create(username="testuser")
        accommodation = Accommodation.objects.create(
            id="acc1",
            feed=1,
            title="Luxury Hotel",
            country_code="BD",
            bedroom_count=3,
            review_score=4.5,
            usd_rate=100.00,
            center=Point(90.4125, 23.8103),
            location=location,
            amenities={"wifi": True, "pool": False},
            user=user,
            published=True
        )
        assert accommodation.id == "acc1"
        assert accommodation.title == "Luxury Hotel"
        assert accommodation.review_score == 4.5
        assert accommodation.amenities == {"wifi": True, "pool": False}
        assert accommodation.location == location
        assert accommodation.user == user


    def test_accommodation_default_values(self):
        location = Location.objects.create(
            id="loc2",
            title="Chittagong",
            center=Point(91.4125, 22.3569),
            country_code="BD"
        )
        accommodation = Accommodation.objects.create(
            id="acc2",
            feed=2,
            title="Budget Inn",
            country_code="BD",
            bedroom_count=1,
            usd_rate=50.00,
            center=Point(91.4125, 22.3569),
            location=location
        )
        assert accommodation.review_score == 0  # Default value
        assert accommodation.published is False  # Default value


@pytest.mark.django_db
class TestLocalizeAccommodationModel:
    def test_create_localized_accommodation(self):
        location = Location.objects.create(
            id="loc1",
            title="Dhaka",
            center=Point(90.4125, 23.8103),
            location_type="city",
            country_code="BD"
        )
        accommodation = Accommodation.objects.create(
            id="acc1",
            title="Luxury Hotel",
            country_code="BD",
            bedroom_count=3,
            usd_rate=150.00,
            center=Point(90.4125, 23.8103),
            location=location
        )
        localized_accommodation = LocalizeAccommodation.objects.create(
            accommodation=accommodation,
            language="en",
            description="A luxury hotel with excellent amenities.",
            policy={"check-in": "2 PM", "check-out": "12 PM"}
        )
        assert localized_accommodation.accommodation == accommodation
        assert localized_accommodation.language == "en"
        assert localized_accommodation.description == "A luxury hotel with excellent amenities."
        assert localized_accommodation.policy == {"check-in": "2 PM", "check-out": "12 PM"}


@pytest.mark.django_db
class TestSignUpView:
    def test_sign_up_get(self):
        """Test that the SignUpView returns a valid response for GET requests."""
        client = Client()
        response = client.get(reverse('signup'))  # Assuming the URL for SignUpView is named 'signup'
        assert response.status_code == 200
        assert 'form' in response.context  # Check that the context contains the form
        assert 'signUp.html' in [t.name for t in response.templates]  # Check if correct template is used


    def test_sign_up_post_invalid(self):
        """Test that an invalid POST request returns the form with errors."""
        client = Client()
        # Prepare invalid data (passwords do not match)
        data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'wrongpassword',
            'email': 'testuser@example.com',
        }
        response = client.post(reverse('signup'), data)
        # Ensure that the form is returned with errors
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors  # Check that there are errors in the form


    def test_sign_up_post_missing_data(self):
        """Test that missing data returns form errors."""
        client = Client()
        # Prepare incomplete data (missing password)
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
        }
        response = client.post(reverse('signup'), data)
        # Ensure that the form is returned with errors
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors 