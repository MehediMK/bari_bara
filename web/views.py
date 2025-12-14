from django.shortcuts import render
from meta.views import Meta

def index(request):
    meta = Meta(
        title='HouseBox - Real Estate Template',
        description='Turning Real Estate Dreams Into Reality',
        keywords=['real estate', 'house', 'apartment'],
        url='/',
        image='/static/img/logo/logo5.png',
        object_type='website',
        site_name='HouseBox',
    )
    return render(request, 'web/index.html', {'meta': meta})

def page(request, pagename):
    from django.template.exceptions import TemplateDoesNotExist
    from django.http import Http404
    
    title = pagename.replace('-', ' ').title()
    meta = Meta(
        title=f'{title} - HouseBox',
        description='Turning Real Estate Dreams Into Reality',
        keywords=['real estate', 'house', 'apartment'],
        url=f'/{pagename}.html',
        image='/static/img/logo/logo5.png',
        object_type='website',
        site_name='HouseBox',
    )

    try:
        return render(request, f'web/{pagename}.html', {'meta': meta})
    except TemplateDoesNotExist:
        raise Http404
