from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with phone as username'

    def handle(self, *args, **kwargs):
        phone = '01531993979'
        first_name = 'Mehedi'
        last_name = 'Khan'
        password = 'Admin123'

        if not User.objects.filter(phone=phone).exists():
            User.objects.create_superuser(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser {phone} created successfully.'))
        else:
            self.stdout.write(f'Superuser {phone} already exists.')
