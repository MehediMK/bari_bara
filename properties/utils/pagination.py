from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(products, page: int, per_page: int = 10):
    paginator_obj = Paginator(products, per_page)
    try:
        items = paginator_obj.page(page)
    except PageNotAnInteger:
        items = paginator_obj.page(1)
    except EmptyPage:
        items = paginator_obj.page(paginator_obj.num_pages)
    return items
