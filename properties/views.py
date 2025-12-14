from django.shortcuts import render, get_object_or_404
from django.db.models import F, Q
from properties.utils import filter_properties, pagination
from .models import Properties, PROPERTY_CATEGORY


def index(request):
    context = {}
    context['request'] = request
    context['property_categories'] = PROPERTY_CATEGORY
    return render(request, 'properties/index.html', context)


SORT_OPTIONS = {
    'price_asc': 'price',
    'price_desc': '-price',
    'newest': '-created_at',
    'largest': '-size',
}


def properties(request):
    context = {}
    page = request.GET.get('page', 1)

    # Get filters from query params
    queryset = filter_properties(request.GET)


    seo_title = "Properties for Sale & Rent - To-Let BD"
    seo_description = "Browse the latest properties for sale and rent across Bangladesh, including apartments, houses, and commercial spaces."
    seo_keywords = "real estate, apartments, flats, houses, Bangladesh property"


    context['properties'] = pagination(queryset, page)
    context['property_categories'] = PROPERTY_CATEGORY
    context['request'] = request
    context['total_count'] = queryset.count()
    context['location_display'] = request.GET.get('location', '').strip() or "All Locations"
    context['sort_by'] = request.GET.get('sort', 'newest')
    # seo tags
    context['seo_title'] = seo_title
    context['seo_description'] = seo_description
    context['seo_keywords'] = seo_keywords
    return render(request, 'properties/properties.html', context)


def property_details(request, slug):
    # Get the main property
    property_obj = get_object_or_404(Properties, slug=slug, is_active=True)

    # Increment view count safely (atomic)
    Properties.objects.filter(pk=property_obj.pk).update(view_count=F('view_count') + 1)

    # Refresh property_obj to get the updated view count
    property_obj.refresh_from_db()

    # Query for similar properties
    similar_properties = (
        Properties.objects.filter(is_active=True)
        .exclude(pk=property_obj.pk)
        .filter(
            Q(district__iexact=property_obj.district, area__iexact=property_obj.area,
              property_type=property_obj.property_type)
            | Q(district__iexact=property_obj.district)
        )
        .order_by('-created_at')[:4]
    )

    seo_title = f"{property_obj.title} in {property_obj.area}, {property_obj.district} - {property_obj.category}"
    seo_description = property_obj.description[:155]  # ideal meta description length
    seo_keywords = f"{property_obj.category}, {property_obj.area}, {property_obj.district}, property for sale, rent"

    context = {
        'property': property_obj,
        'similar_properties': similar_properties,
        # seo tags
        'seo_title': seo_title,
        'seo_description': seo_description,
        'seo_keywords': seo_keywords,
    }

    return render(request, 'properties/property_details.html', context)


def services(request):
    return render(request, 'properties/services.html')


def contact(request):
    return render(request, 'properties/contact.html')


def service_details(request):
    return render(request, 'properties/service_details.html')


def blog(request):
    return render(request, 'properties/blog.html')


def blog_details(request):
    return render(request, 'properties/blog_details.html')


def agents(request):
    return render(request, 'properties/agents.html')


def agent_profile(request):
    return render(request, 'properties/agent_profile.html')


def terms(request):
    return render(request, 'properties/terms.html')


def privacy(request):
    return render(request, 'properties/privacy.html')


def about(request):
    return render(request, 'properties/about.html')


def starter_page(request):
    return render(request, 'properties/starter_page.html')

