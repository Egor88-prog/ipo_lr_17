from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from io import BytesIO
import openpyxl

from .models import Product, Category, Manufacture
from users.models import Cart, CartItem
from .models import Order, OrderItem




def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

def product_list(request):
    products = Product.objects.select_related(
        'category',
        'manufacture'
    ).all()

    category_id = request.GET.get('category')
    manufacture_id = request.GET.get('manufacture')
    search_query = request.GET.get('q')

    if category_id:
        products = products.filter(category_id=category_id)

    if manufacture_id:
        products = products.filter(manufacture_id=manufacture_id)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(descriptions__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'manufactures': Manufacture.objects.all(),
    }

    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('category', 'manufacture'),
        pk=pk
    )

    return render(request, 'shop/product_detail.html', {
        'product': product
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_user_cart(request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity < product.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            raise ValidationError(
                f"Доступно только {product.quantity} шт."
            )

    return redirect('cart')

@login_required
def update_cart(request, item_id):
    cart = get_user_cart(request.user)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))

            if quantity <= 0:
                cart_item.delete()
            elif quantity <= cart_item.product.quantity:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                raise ValidationError(
                    f"Максимум доступно: {cart_item.product.quantity}"
                )

        except (ValueError, ValidationError):
            pass

    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart = get_user_cart(request.user)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    cart_item.delete()
    return redirect('cart')

@login_required
def cart_view(request):
    cart = get_user_cart(request.user)

    cart_items = cart.items.select_related('product')

    total_price = sum(
        item.item_total_price() for item in cart_items
    )

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'shop/cart.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
@transaction.atomic
def checkout(request):
    cart = get_user_cart(request.user)
    cart_items = cart.items.select_related('product')

    if not cart_items.exists():
        return redirect('cart')

    order = Order.objects.create(
        user=request.user,
        created_at=timezone.now()
    )

    total_price = 0

    for item in cart_items:
        if item.quantity > item.product.quantity:
            raise ValidationError(
                f"Недостаточно товара: {item.product.name}"
            )

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        # уменьшаем количество товара на складе
        item.product.quantity -= item.quantity
        item.product.save()

        total_price += item.quantity * item.product.price

    order.total_price = total_price
    order.save()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Receipt"

    sheet.append(["Чек №", order.id])
    sheet.append(["Дата", order.created_at.strftime("%Y-%m-%d %H:%M")])
    sheet.append([])
    sheet.append(["Товар", "Количество", "Цена", "Сумма"])

    for item in order.items.all():
        sheet.append([
            item.product.name,
            item.quantity,
            float(item.price),
            float(item.quantity * item.price)
        ])

    sheet.append([])
    sheet.append(["ИТОГО", "", "", float(total_price)])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    print("USER EMAIL:", request.user.email)

    email = EmailMessage(
        subject=f"Ваш заказ №{order.id}",
        body="Спасибо за покупку! Чек во вложении.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[request.user.email],
    )

    email.attach(
        f"receipt_{order.id}.xlsx",
        buffer.read(),
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    email.send()

    cart.items.all().delete()

    return render(request, 'shop/checkout_success.html', {
        'order': order
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})