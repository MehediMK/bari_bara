from django.db.models import Q
from properties.models import Properties


SORT_OPTIONS = {
    'price_asc': 'price',
    'price_desc': '-price',
    'newest': '-created_at',
    'largest': '-size',
}


def filter_properties(query_params):
    """
    Returns a filtered & sorted queryset of approved + active Properties
    based on request.GET query params.
    """
    queryset = Properties.objects.filter(status='approved', is_active=True)

    location = query_params.get('location', '').strip()
    property_type = query_params.get('type', '')
    price_range = query_params.get('price', '')
    bedrooms = query_params.get('bedrooms', '')
    sort_by = query_params.get('sort', 'newest')

    if location:
        queryset = queryset.filter(
            Q(district__icontains=location) |
            Q(area__icontains=location) |
            Q(sub_area__icontains=location) |
            Q(zip_code__icontains=location)
        )

    if property_type:
        queryset = queryset.filter(
            Q(category=property_type) |
            Q(property_type=property_type)
        )

    if price_range:
        if price_range == '0-500k':
            queryset = queryset.filter(price__lte=500000)
        elif price_range == '500k-1m':
            queryset = queryset.filter(price__gt=500000, price__lte=1000000)
        elif price_range == '1m+':
            queryset = queryset.filter(price__gt=1000000)

    if bedrooms and bedrooms.isdigit():
        queryset = queryset.filter(bedroom__gte=int(bedrooms))

    # Apply sort
    queryset = queryset.order_by(SORT_OPTIONS.get(sort_by, '-created_at'))

    return queryset
