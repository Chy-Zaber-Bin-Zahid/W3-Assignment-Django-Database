# Generated by Django 5.1.3 on 2024-12-02 10:45

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('location_type', models.CharField(choices=[('country', 'Country'), ('state', 'State'), ('city', 'City')], default='city', max_length=20)),
                ('country_code', models.CharField(max_length=2)),
                ('state_abbr', models.CharField(blank=True, max_length=3, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='properties.location')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('feed', models.PositiveSmallIntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('country_code', models.CharField(max_length=2)),
                ('bedroom_count', models.PositiveIntegerField()),
                ('review_score', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('usd_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('amenities', models.JSONField(blank=True, null=True)),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accommodations', to='properties.location')),
            ],
            options={
                'verbose_name': 'Accommodation',
                'verbose_name_plural': 'Accommodations',
            },
        ),
        migrations.CreateModel(
            name='LocalizeAccommodation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(max_length=2)),
                ('description', models.TextField()),
                ('policy', models.JSONField(blank=True, null=True)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localized', to='properties.accommodation')),
            ],
            options={
                'verbose_name': 'Localized Accommodation',
                'verbose_name_plural': 'Localized Accommodations',
                'unique_together': {('accommodation', 'language')},
            },
        ),
    ]
