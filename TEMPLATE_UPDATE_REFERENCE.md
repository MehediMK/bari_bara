# Quick Template Update Reference

## Property Listing Template (`sidebar-grid.html`)

### Replace This Section (Lines ~68-295):
```html
<div class="col-lg-6 col-md-6">
  <div class="property-boxarea">
    <!-- Hardcoded property card -->
  </div>
</div>
```

### With This Dynamic Loop:
```django
{% load static %}
{% for prop in properties %}
<div class="col-lg-6 col-md-6">
  <div class="property-boxarea">
    <!-- Property Image -->
    <div class="img1 image-anime">
      {% if prop.images.exists %}
        {% with prop.images.first as img %}
        <img src="{{ img.image.url }}" alt="{{ prop.title }}">
        {% endwith %}
      {% else %}
        <img src="{% static 'img/all-images/properties/property-img2.png' %}" alt="{{ prop.title }}">
      {% endif %}
    </div>
    
    <!-- Category Tags -->
    <div class="category-list">
      <ul>
        {% if prop.featured %}<li><a href="#">Featured</a></li>{% endif %}
        <li><a href="#">{{ prop.get_category_display }}</a></li>
      </ul>
    </div>
    
    <!-- Property Info -->
    <div class="content-area">
      <a href="{% url 'properties:detail' prop.slug %}">{{ prop.title }}</a>
      <div class="space18"></div>
      <p>{{ prop.district }}, {{ prop.area }}</p>
      <div class="space24"></div>
      <ul>
        <li><a href="#"><img src="{% static 'img/icons/bed1.svg' %}" alt="">x{{ prop.bedroom }}</a></li>
        <li><a href="#"><img src="{% static 'img/icons/bath1.svg' %}" alt="">x{{ prop.bathroom }}</a></li>
        {% if prop.size %}<li><a href="#"><img src="{% static 'img/icons/sqare1.svg' %}" alt="">{{ prop.size }} {{ prop.size_unit }}</a></li>{% endif %}
      </ul>
      <div class="btn-area">
        <a href="#" class="nm-btn">{{ prop.currency }} {{ prop.price|floatformat:0 }}</a>
        <a href="javascript:void(0)" class="heart">
          <img src="{% static 'img/icons/heart1.svg' %}" alt="" class="heart1">
          <img src="{% static 'img/icons/heart2.svg' %}" alt="" class="heart2">
        </a>
      </div>
    </div>
  </div>
</div>
{% empty %}
<div class="col-12">
  <p class="text-center">No properties found. Try adjusting your filters.</p>
</div>
{% endfor %}
```

### Update Property Count (Line ~16):
```django
<h3>Properties ({{ total_count }})</h3>
```

### Add Pagination (After property loop, Line ~296):
```django
<div class="col-lg-12">
  {% include "components/pagination.html" %}
</div>
```

---

## Property Detail Template (`property-details-v3.html`)

### Update Hero Title (Line ~6):
```django
{% include "components/hero.html" with title=property.title %}
```

### Update Property Images (Lines ~17-21):
```django
<div class="img2-carousel owl-carousel">
  {% for img in property.images.all %}
  <img src="{{ img.image.url }}" alt="{{ property.title }}">
  {% endfor %}
</div>
```

### Update Property Title & Price (Lines ~68-72):
```django
<h2>{{ property.title }}</h2>
<ul>
  <li><a href="#">{{ property.currency }} {{ property.price|floatformat:0 }}</a></li>
  <li><a href="#">/{{ property.get_pay_duration_display }}</a></li>
</ul>
```

### Update Property Features (Lines ~79-81):
```django
<li><a href="#"><img src="{% static 'img/icons/bed1.svg' %}">x{{ property.bedroom }}</a></li>
<li><a href="#"><img src="{% static 'img/icons/bath1.svg' %}">x{{ property.bathroom }}</a></li>
<li><a href="#"><img src="{% static 'img/icons/sqare1.svg' %}">{{ property.size }} {{ property.size_unit }}</a></li>
```

### Update Location (Line ~88):
```django
<li><a href="#"><svg>...</svg> {{ property.district }}, {{ property.area }}, {{ property.country }}</a></li>
```

### Update Description (Add after line ~105):
```django
<h3>Property Description</h3>
<div class="space32"></div>
<p>{{ property.description|linebreaks }}</p>
<div class="space60"></div>
```

### Update Amenities (Lines ~117-295):
```django
<h3>{{ property.title }} Amenities</h3>
<div class="space12"></div>
<div class="row">
  {% for amenity in property.all_amenities.all %}
  <div class="col-lg-6 col-md-6">
    <div class="list-box">
      <div class="icon">
        <!-- Use amenity.icon if available -->
        <svg>...</svg>
      </div>
      <div class="text">
        <p>{{ amenity.name }}</p>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
```

### Update Owner Contact (Lines ~471-487):
```django
<h4>Contact Owner</h4>
<div class="space24"></div>
<div class="personal-info">
  <div class="img1">
    {% if property.user.profile_picture %}
    <img src="{{ property.user.profile_picture.url }}" alt="{{ property.user.get_full_name }}">
    {% else %}
    <img src="{% static 'img/all-images/blog/blog-img17.png' %}" alt="{{ property.user.get_full_name }}">
    {% endif %}
  </div>
  <div class="content">
    <a href="#">{{ property.user.get_full_name }}</a>
    {% if property.user.email %}
    <a href="mailto:{{ property.user.email }}">
      <svg>...</svg>{{ property.user.email }}
    </a>
    {% endif %}
    <a href="tel:{{ property.phone }}">
      <svg>...</svg>{{ property.phone }}
    </a>
  </div>
</div>
```

### Update Map Location (Lines ~321-345):
```django
<h3>Map Location</h3>
<div class="space32"></div>
<div class="map-section">
  {% if property.latitude and property.longitude %}
  <iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d{{ property.latitude }}!2d{{ property.longitude }}" 
          width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
  {% else %}
  <p>Map not available</p>
  {% endif %}
  <div class="space12"></div>
  <div class="list">
    <ul>
      <li><span>Address:</span><div>{{ property.short_address }}</div></li>
      <li><span>District:</span><div>{{ property.district }}</div></li>
    </ul>
    <ul class="m-0">
      <li><span>Postal Code:</span><div>{{ property.zip_code|default:"N/A" }}</div></li>
      <li><span>Area:</span><div>{{ property.area }}</div></li>
    </ul>
  </div>
</div>
```

---

## Common Template Filters

```django
{{ property.price|floatformat:0 }}           # 25000.00 → 25000
{{ property.price|intcomma }}                # 25000 → 25,000 (needs {% load humanize %})
{{ property.description|truncatewords:50 }}  # Limit to 50 words
{{ property.description|linebreaks }}        # Convert newlines to <p> tags
{{ property.created_at|date:"F d, Y" }}      # January 23, 2026
{{ property.get_category_display }}          # 'family' → 'Family'
```

---

## Template Tags to Add

At the top of each template:
```django
{% extends 'base.html' %}
{% load static %}
{% load humanize %}  {# For intcomma filter #}
```

---

## URL Patterns

```django
{% url 'properties:list' %}                  # /properties/
{% url 'properties:detail' property.slug %}  # /properties/flat-2bed-dhaka-dhanmondi-12345/
{% url 'web:index' %}                        # / (homepage)
```

---

## Conditional Rendering

```django
{% if property.images.exists %}
  <!-- Show images -->
{% else %}
  <!-- Show placeholder -->
{% endif %}

{% if property.featured %}
  <span class="badge">Featured</span>
{% endif %}

{% if property.is_negotiable %}
  <span>Negotiable</span>
{% endif %}
```

---

## Loop Examples

```django
{# Property Images #}
{% for img in property.images.all %}
  <img src="{{ img.image.url }}" alt="{{ img.name }}">
{% endfor %}

{# Amenities #}
{% for amenity in property.all_amenities.all %}
  <li>{{ amenity.name }}</li>
{% endfor %}

{# Similar Properties #}
{% for similar in similar_properties %}
  {% include "components/property_card.html" with property=similar %}
{% endfor %}
```

---

## Quick Test

After updating templates, test:
1. `/properties/` - Should show dynamic listing
2. Click any property - Should show detail page
3. Use filters - Should filter results
4. Click pagination - Should navigate pages

---

**Pro Tip:** Use browser DevTools to inspect the page and verify data is rendering correctly!
