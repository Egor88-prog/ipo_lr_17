from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config


class Command(BaseCommand):
    help = 'Creates superuser from env vars'

    def handle(self, *args, **options):
        username = config('DJANGO_SU_USERNAME', default='admin')
        email = config('DJANGO_SU_EMAIL', default='admin@example.com')
        password = config('DJANGO_SU_PASSWORD', default='admin123')

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        if created:
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            user.profile.role = 'ADMIN'
            user.profile.save()
            self.stdout.write(f'Superuser "{username}" created')
        else:
            user.profile.role = 'ADMIN'
            user.profile.save()
            self.stdout.write(f'Superuser "{username}" already exists, role updated')
