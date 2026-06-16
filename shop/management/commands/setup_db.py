from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from decouple import config
from users.models import Cart, Profile
from users.signals import create_user_related
from shop.models import Category, Manufacture, Product, Order, OrderItem


class Command(BaseCommand):
    help = 'Clears DB, loads data.json, creates superuser'

    def handle(self, *args, **options):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Cart.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Manufacture.objects.all().delete()

        post_save.disconnect(create_user_related, sender=User)
        call_command('loaddata', 'data.json')
        post_save.connect(create_user_related, sender=User)

        username = config('DJANGO_SU_USERNAME', default='admin')
        email = config('DJANGO_SU_EMAIL', default='admin@example.com')
        password = config('DJANGO_SU_PASSWORD', default='admin123')

        user, created = User.objects.get_or_create(
            username=username, defaults={'email': email}
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
            self.stdout.write(f'Superuser "{username}" already exists')
