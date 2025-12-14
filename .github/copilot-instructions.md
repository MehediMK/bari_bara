# HouseBox Django Project - AI Coding Guidelines

## Architecture Overview
HouseBox is a Django-based real estate platform with three main apps:
- `accounts`: Custom user model with phone-based auth, roles (owner/freelancer/visitor/admin), and extended profiles
- `properties`: Property listings with filtering, images, amenities, and SEO-friendly slugs
- `web`: Static page views using generic template handler

Key data flows: Users (owners) create Properties → Properties link to Amenities and PropertyImages → Views use utils for filtering/pagination.

## Critical Workflows
- **Run server**: `python manage.py runserver` (serves on 0.0.0.0:8000)
- **Create admin**: `python manage.py createadmin` (creates superuser with phone 01531993979)
- **Load fixtures**: `python manage.py loaddata properties/fixtures/amenities_fixture.json properties/fixtures/properties_fixture.json`
- **Migrations**: Standard Django `makemigrations` and `migrate`

## Project-Specific Patterns
- **Custom User**: Phone as USERNAME_FIELD, roles via `role` field, properties like `user.is_owner`
- **Property Slugs/Titles**: Auto-generated in `Properties.save()` using category/type/bedrooms/location/code
- **Filtering**: Use `properties.utils.filtering.filter_properties(request.GET)` for query params (location/type/price/bedrooms/sort)
- **Pagination**: `properties.utils.pagination.pagination(queryset, page, per_page=10)`
- **SEO Meta**: Pass `Meta` object to templates or use context vars (seo_title/description/keywords)
- **Templates**: Extend `base.html`, include components from `templates/components/`, use `{% load static %}` and `{% url %}`
- **Admin**: Uses django-unfold for enhanced UI

## Examples
- **Add property view**: In `properties/views.py`, filter with `filter_properties(request.GET)`, paginate with `pagination()`, render `properties/properties.html`
- **User signup**: In `accounts/views.py`, use `SignUpForm` with phone/password, redirect to 'properties'
- **Property detail**: Increment view_count atomically with `F('view_count') + 1`, find similar via Q queries on district/area/type

## Key Files
- `housebox/settings.py`: INSTALLED_APPS, AUTH_USER_MODEL, META_* settings
- `accounts/models.py`: User with phone auth, roles, points
- `properties/models.py`: Properties with auto-slug/title, Amenities, PropertyImage
- `properties/utils/`: filtering.py and pagination.py for reusable logic
- `templates/base.html`: SEO meta tags, component includes
- `requirements.txt`: Core deps (Django 5.2.9, django-countries, django-meta, django-unfold, pillow)</content>
<parameter name="filePath">/home/mehedi/Desktop/mehedi/credentials/django/bari_bara/.github/copilot-instructions.md