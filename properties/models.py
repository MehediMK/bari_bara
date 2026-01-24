from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField


User = get_user_model()

PROPERTY_CATEGORY = [
    ('family', 'Family'),
    ('bachelor', 'Bachelor'),
    ('sublet', 'Sublet'),
    ('hostel', 'Hostel'),
    ('mess', 'Mess'),
    ('office', 'Office Space'),
    ('shop', 'Shop / Retail Space'),
    ('warehouse', 'Warehouse'),
    ('factory', 'Factory / Industrial Unit'),
]

PROPERTY_TYPES = [
    ('flat', 'Flat / Apartment'),
    ('floor', 'Floor'),
    ('room', 'Room'),
    ('seat', 'Seat (Hostel/Mess)'),
    ('house', 'House / Villa'),
    ('unit', 'Unit'),
]

GENDER_PREFERENCES = [
    ('male', 'Male only'),
    ('female', 'Female only'),
    ('any', 'Any'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('expired', 'Expired'),
]

PAY_DURATION = [
    ('month', 'Month'),
    ('quarter', 'Quarter'),
    ('year', 'Year'),
    ('contract', 'Contract'),
]

SIZE_UNIT_CHOICES = [
    ('sqft', 'Square feet'),
    ('sqm', 'Square meters'),
]


class Amenity(models.Model):
    """
    Master list of available amenities.
    """
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional: CSS class or icon for display."
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Properties(models.Model):
    """
    Main rental unit Properties.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')

    # Basic info
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=PROPERTY_CATEGORY)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    available_from = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_PREFERENCES, default='any')

    # Property details
    bedroom = models.PositiveSmallIntegerField(default=0)
    bathroom = models.PositiveSmallIntegerField(default=0)
    balcony = models.PositiveSmallIntegerField(default=0)
    parking = models.PositiveSmallIntegerField(default=0)
    others_room = models.PositiveSmallIntegerField(default=0)
    floor_no = models.PositiveSmallIntegerField(default=0)
    size = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    size_unit = models.CharField(max_length=10, choices=SIZE_UNIT_CHOICES, default='sqft', blank=True, null=True)

    # Address
    country = CountryField(blank_label='_(Select country)', default='BD')
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    sub_area = models.CharField(max_length=100)
    short_address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Contact
    phone = models.CharField(_('Contact Number'), max_length=20)

    # Price & Duration
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="BDT")
    pay_duration = models.CharField(max_length=10, choices=PAY_DURATION, default='month')

    # Status & Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    included_in_price_amenities = models.ManyToManyField(Amenity, blank=True, related_name='included_in_properties')
    property_code = models.CharField(max_length=20, unique=True, blank=True)
    featured = models.BooleanField(default=False)

    all_amenities = models.ManyToManyField(Amenity, related_name='properties')
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_negotiable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    updated_at = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        if not self.property_code:
            import random
            self.property_code = str(random.randint(10000, 99999)) + str(self.pk or '')
        if not self.slug:
            # build slug components
            components = [
                self.category,
                self.property_type,
                f"{self.bedroom}bed" if self.bedroom else None,
                self.district,
                self.area,
                self.property_code
            ]
            raw_slug = "-".join(str(c).replace(" ", "-") for c in components if c)
            self.slug = slugify(raw_slug)[:60]  # limit to 60 chars
        if not self.title:
            # Update title
            available_date = self.available_from.strftime("%B") if self.available_from else "Immediate"
            title_components = [
                'Rent From',
                available_date,
                'for',
                self.category,
                self.property_type,
                f"{self.bedroom}bed",
                'in',
                self.district,
                self.area
            ]
            self.title = " ".join(str(c) for c in title_components if c)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.district}/{self.area})"
    
    @property
    def address(self):
        """
        Full formatted address for display
        """
        parts = [
            self.short_address,
            self.sub_area,
            self.area,
            self.district,
            self.division,
            self.country.name if self.country else None,
            self.zip_code,
        ]
        return ", ".join([p for p in parts if p])


class PropertyImage(models.Model):
    property = models.ForeignKey(Properties, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='property_images/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.property.title}"
