from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import Amenity, Properties, PropertyImage


@admin.register(Amenity)
class AmenityAdmin(ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)
    ordering = ('name',)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Properties)
class PropertiesAdmin(ModelAdmin):
    list_display = (
        'title', 'user', 'district', 'price', 'status', 'created_at', 'featured'
    )
    list_filter = (
        'status', 'category', 'property_type', 'created_at', 'featured'
    )
    search_fields = ('title', 'district', 'area', 'property_code')
    readonly_fields = ('title', 'created_at', 'updated_at', 'view_count', 'property_code', 'slug')

    inlines = [PropertyImageInline]

    filter_horizontal = ('included_in_price_amenities', 'all_amenities')
    CheckboxSelectMultiple = True
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'user', 'title', 'slug', 'category', 'property_type',
                'available_from', 'gender', 'featured', 'is_active',
            )
        }),
        ('Property Details', {
            'classes': ('collapse',),
            'fields': (
                'bedroom', 'bathroom', 'balcony', 'parking', 'others_room',
                'floor_no', 'size', 'size_unit'
            )
        }),
        ('Location & Address', {
            'classes': ('collapse',),
            'fields': (
                'country', 'division', 'district', 'area', 'sub_area',
                'short_address', 'zip_code', 'latitude', 'longitude'
            )
        }),
        ('Contact & Pricing', {
            'classes': ('collapse',),
            'fields': (
                'phone', 'price', 'currency', 'deposit_amount',
                'is_negotiable', 'pay_duration'
            )
        }),
        ('Amenities', {
            'classes': ('collapse',),
            'fields': ('included_in_price_amenities', 'all_amenities', 'description',)
        }),
        ('Meta & Status', {
            'classes': ('collapse',),
            'fields': (
                'property_code', 'status', 'view_count',
                'created_at', 'updated_at'
            )
        }),
    )
