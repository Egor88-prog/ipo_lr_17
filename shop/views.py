from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from io import BytesIO
import openpyxl
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Product, Category, Manufacture
from users.models import Cart, CartItem, Profile
from .models import Order, OrderItem
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ManufacturerSerializer,
    CartSerializer,
    CartItemSerializer,
    ProfileSerializer,
    OrderSerializer,
    OrderItemSerializer
)

def index(request):
    products = Product.objects.all()[:6]
    categories = Category.objects.all()

    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories
    })


def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

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

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=False, label='Имя',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, required=False, label='Телефон',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False, label='Адрес',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    city = forms.CharField(max_length=100, required=False, label='Город доставки',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(max_length=20, required=False, label='Индекс',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'full_name', 'phone', 'address', 'city', 'postal_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile
            profile.full_name = self.cleaned_data.get('full_name', '')
            profile.phone = self.cleaned_data.get('phone', '')
            profile.address = self.cleaned_data.get('address', '')
            profile.city = self.cleaned_data.get('city', '')
            profile.postal_code = self.cleaned_data.get('postal_code', '')
            profile.save()
        return user


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()

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


@login_required
def profile_view(request):
    return render(request, 'shop/profile.html')


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


class BootstrapPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


@login_required
def settings_view(request):
    msg = ''
    msg_type = ''
    if request.method == 'POST':
        form = BootstrapPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            msg = 'Пароль успешно изменён'
            msg_type = 'success'
        else:
            msg = 'Исправьте ошибки в форме'
            msg_type = 'danger'
    else:
        form = BootstrapPasswordChangeForm(request.user)
    return render(request, 'shop/settings.html', {
        'form': form,
        'msg': msg,
        'msg_type': msg_type,
    })


from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.is_authenticated and request.user.profile.role == 'ADMIN'


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'ADMIN'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacture.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        if user.profile.role == 'ADMIN':
            return Order.objects.all()
        return Order.objects.filter(user=user)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me(request):
    profile = request.user.profile
    if request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


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

    # ✅ Пагинация (9 товаров)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'manufactures': Manufacture.objects.all(),
    }

    return render(request, 'shop/product_list.html', context)