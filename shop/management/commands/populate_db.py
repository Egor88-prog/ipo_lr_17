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

        cat1 = Category.objects.create(name='Термосы')
        cat2 = Category.objects.create(name='Кружки')
        cat3 = Category.objects.create(name='Аксессуары')

        man1 = Manufacture.objects.create(name='ThermoPro')
        man2 = Manufacture.objects.create(name='HeatMaster')
        man3 = Manufacture.objects.create(name='CoolFlask')

        products = [
            Product(name='Термос 1л', descriptions='Нержавеющая сталь, сохраняет тепло 12ч',
                    category=cat1, manufacture=man1, price=1500, quantity=50),
            Product(name='Термос 0.5л', descriptions='Компактный, для походов',
                    category=cat1, manufacture=man2, price=900, quantity=30),
            Product(name='Термос 2л', descriptions='Большой для семьи',
                    category=cat1, manufacture=man3, price=2500, quantity=20),
            Product(name='Кружка термо', descriptions='С двойными стенками, 400мл',
                    category=cat2, manufacture=man1, price=700, quantity=40),
            Product(name='Кружка дорожная', descriptions='Герметичная крышка, 300мл',
                    category=cat2, manufacture=man2, price=500, quantity=60),
            Product(name='Набор насадок', descriptions='Для разных типов напитков',
                    category=cat3, manufacture=man3, price=300, quantity=100),
            Product(name='Чехол для термоса', descriptions='Неопреновый, для 1л',
                    category=cat3, manufacture=man1, price=400, quantity=80),
            Product(name='Фильтр для чая', descriptions='Сетчатый, нержавейка',
                    category=cat3, manufacture=man2, price=200, quantity=150),
        ]
        Product.objects.bulk_create(products)
        self.stdout.write(f'Created {len(products)} products')
