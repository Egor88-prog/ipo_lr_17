from django.core.management.base import BaseCommand
from shop.models import Category, Manufacture, Product, Order, OrderItem


class Command(BaseCommand):
    help = 'Populates DB with sample data'

    def handle(self, *args, **options):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Manufacture.objects.all().delete()

        cat_drink = Category.objects.create(name='Термосы для напитков')
        cat_food = Category.objects.create(name='Термосы для еды')
        cat_mug = Category.objects.create(name='Термокружки')
        cat_travel = Category.objects.create(name='Туристические термосы')
        cat_kids = Category.objects.create(name='Детские термосы')
        cat_sport = Category.objects.create(name='Спортивные бутылки')
        cat_vacuum = Category.objects.create(name='Вакуумные термосы')
        cat_metal = Category.objects.create(name='Металлические термосы')
        cat_large = Category.objects.create(name='Термосы большого объёма')
        cat_compact = Category.objects.create(name='Компактные термосы')

        man_tefal = Manufacture.objects.create(name='Tefal')
        man_thermos = Manufacture.objects.create(name='Thermos')
        man_zojirushi = Manufacture.objects.create(name='Zojirushi')
        man_stanley = Manufacture.objects.create(name='Stanley')
        man_xiaomi = Manufacture.objects.create(name='Xiaomi')

        products = [
            Product(name='Термос Thermos Stainless King 0.5 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_vacuum, manufacture=man_thermos, price=263, quantity=50),
            Product(name='Термос Thermos Stainless King 1.0 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_thermos, price=230, quantity=89),
            Product(name='Термос Tefal Senator 0.7 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_sport, manufacture=man_tefal, price=91, quantity=80),
            Product(name='Термос Tefal Travel Mug 0.36 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_vacuum, manufacture=man_tefal, price=72, quantity=77),
            Product(name='Термос Stanley Classic 0.75 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_kids, manufacture=man_stanley, price=202, quantity=61),
            Product(name='Термос Stanley Legendary 1.0 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_kids, manufacture=man_stanley, price=268, quantity=46),
            Product(name='Термос Zojirushi SM-SD48 0.48 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_metal, manufacture=man_zojirushi, price=75, quantity=37),
            Product(name='Термос Zojirushi SJ-TG10 1.0 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_large, manufacture=man_zojirushi, price=226, quantity=46),
            Product(name='Термокружка Xiaomi Kiss Kiss Fish 0.43 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_xiaomi, price=181, quantity=87),
            Product(name='Термокружка Tefal City Mug 0.35 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_kids, manufacture=man_tefal, price=200, quantity=84),
            Product(name='Термос пищевой Thermos FBB 0.75 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_compact, manufacture=man_thermos, price=186, quantity=47),
            Product(name='Термос туристический Stanley Adventure 1.3 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_vacuum, manufacture=man_stanley, price=257, quantity=98),
            Product(name='Термос для еды Thermos King Food Jar 0.47 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_travel, manufacture=man_thermos, price=173, quantity=30),
            Product(name='Термос детский Zojirushi SC-ZT45',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_large, manufacture=man_zojirushi, price=252, quantity=68),
            Product(name='Термокружка Stanley Trigger Action 0.47 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_stanley, price=65, quantity=61),
            Product(name='Термос Tefal Grand 1.2 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_large, manufacture=man_tefal, price=139, quantity=55),
            Product(name='Термос Thermos Light & Compact 1.0 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_thermos, price=131, quantity=53),
            Product(name='Термос вакуумный Zojirushi SF-CC20 2.0 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_kids, manufacture=man_zojirushi, price=167, quantity=61),
            Product(name='Термос Stanley Master Series 0.53 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_metal, manufacture=man_stanley, price=283, quantity=63),
            Product(name='Термос для напитков Thermos JNL 0.5 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_thermos, price=211, quantity=30),
            Product(name='Термокружка Xiaomi Viomi Steel 0.46 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_sport, manufacture=man_xiaomi, price=200, quantity=75),
            Product(name='Термос Tefal Ultimate 0.5 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_kids, manufacture=man_tefal, price=212, quantity=75),
            Product(name='Термос Stanley Classic 1.4 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_stanley, price=212, quantity=50),
            Product(name='Термос Zojirushi SM-SA60 0.6 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_zojirushi, price=130, quantity=81),
            Product(name='Термос Thermos Work Series 1.2 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_thermos, price=231, quantity=62),
            Product(name='Термос туристический Stanley Adventure 0.73 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_stanley, price=314, quantity=83),
            Product(name='Термос для чая Tefal Coffee To Go 0.4 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_compact, manufacture=man_tefal, price=227, quantity=44),
            Product(name='Термокружка Thermos Guardian 0.5 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_vacuum, manufacture=man_thermos, price=116, quantity=42),
            Product(name='Термос Zojirushi Stainless Bottle 0.8 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_sport, manufacture=man_zojirushi, price=155, quantity=91),
            Product(name='Термос Stanley Mountain 1.0 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_stanley, price=102, quantity=25),
            Product(name='Термос Tefal Outdoor 0.9 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_drink, manufacture=man_tefal, price=169, quantity=32),
            Product(name='Термос Thermos Element 1.0 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_vacuum, manufacture=man_thermos, price=179, quantity=39),
            Product(name='Термокружка Stanley Go Series 0.47 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_metal, manufacture=man_stanley, price=228, quantity=83),
            Product(name='Термос Zojirushi SJ-JS10 1.03 л',
                    descriptions='Нержавеющая сталь, сохраняет тепло до 12 часов и холод до 24 часов.',
                    category=cat_large, manufacture=man_zojirushi, price=320, quantity=29),
        ]
        Product.objects.bulk_create(products)
        self.stdout.write(f'Created {len(products)} products')
