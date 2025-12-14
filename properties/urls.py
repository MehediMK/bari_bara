from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('properties/', views.properties, name='properties'),
    path('property-details/<str:slug>/', views.property_details, name='property_details'),
    path('services/', views.services, name='services'),
    path('service-details/', views.service_details, name='service_details'),
    path('blog/', views.blog, name='blog'),
    path('blog-details/', views.blog_details, name='blog_details'),
    path('agents/', views.agents, name='agents'),
    path('agent-profile/', views.agent_profile, name='agent_profile'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('about/', views.about, name='about'),
    path('starter-page/', views.starter_page, name='starter_page'),
]