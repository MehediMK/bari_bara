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

    # Search / Keyword
    keyword = query_params.get('keyword', '').strip()
    if keyword:
        queryset = queryset.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    # Location
    location = query_params.get('location', '').strip()
    if location:
        queryset = queryset.filter(
            Q(district__icontains=location) |
            Q(area__icontains=location) |
            Q(sub_area__icontains=location) |
            Q(short_address__icontains=location) |
            Q(zip_code__icontains=location)
        )

    # Property Type / Category
    property_type = query_params.get('type', '') or query_params.get('category', '')
    if property_type:
        queryset = queryset.filter(
            Q(category__iexact=property_type) |
            Q(property_type__iexact=property_type)
        )

    # Price Range (preset or min/max)
    price_range = query_params.get('price_range', '')
    min_price = query_params.get('min_price')
    max_price = query_params.get('max_price')

    if min_price and min_price.isdigit():
        queryset = queryset.filter(price__gte=min_price)
    if max_price and max_price.isdigit():
        queryset = queryset.filter(price__lte=max_price)
    
    # Handle preset ranges if min/max not strictly provided
    if not (min_price or max_price) and price_range:
        if price_range == '0-500k':
            queryset = queryset.filter(price__lte=500000)
        elif price_range == '500k-1m':
            queryset = queryset.filter(price__gt=500000, price__lte=1000000)
        elif price_range == '1m+':
            queryset = queryset.filter(price__gt=1000000)

    # Beds & Baths
    bedrooms = query_params.get('bedrooms', '')
    if bedrooms and bedrooms.isdigit():
        queryset = queryset.filter(bedroom__gte=int(bedrooms))

    bathrooms = query_params.get('bathrooms', '')
    if bathrooms and bathrooms.isdigit():
        queryset = queryset.filter(bathroom__gte=int(bathrooms))

    # Size
    min_size = query_params.get('min_size', '')
    max_size = query_params.get('max_size', '')
    
    if min_size and min_size.isdigit():
        queryset = queryset.filter(size__gte=int(min_size))
    if max_size and max_size.isdigit():
        queryset = queryset.filter(size__lte=int(max_size))

    # Apply sort
    sort_by = query_params.get('sort', 'newest')
    queryset = queryset.order_by(SORT_OPTIONS.get(sort_by, '-created_at'))

    return queryset
