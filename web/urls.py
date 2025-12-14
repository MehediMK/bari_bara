from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:pagename>.html', views.page, name='page'),
]
