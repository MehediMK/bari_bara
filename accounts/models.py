from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


USER_ROLES = [
    ('owner', 'Homeowner'),
    ('freelancer', 'Freelancer / Affiliate'),
    ('visitor', 'Visitor / Renter'),
    ('admin', 'Admin'),
]
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('The Phone number must be set'))
        extra_fields.setdefault('is_active', True)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """
    Extends Django's User.
    """
    username = None  # ✅ remove username field
    phone = models.CharField(_('Phone number'), max_length=20, unique=True)
    email = models.EmailField(_('Email address'), unique=True, blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    nid_number = models.CharField(max_length=20, blank=True, null=True)
    nid_file = models.FileField(upload_to='nid/', blank=True, null=True)

    country = models.CharField(max_length=100, blank=True)
    division = models.CharField(_("division / state"), max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    sub_area = models.CharField(max_length=100, blank=True, null=True)
    short_address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True)

    role = models.CharField(max_length=20, choices=USER_ROLES, default='visitor')
    is_verified = models.BooleanField(default=False)

    points_balance = models.IntegerField(default=0, help_text="Earned points (for freelancers/visitors)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_owner(self):
        return self.role == 'owner'

    @property
    def is_freelancer(self):
        return self.role == 'freelancer'

    @property
    def is_renter(self):
        return self.role == 'visitor'

    @property
    def is_admin_user(self):
        return self.role == 'admin'
