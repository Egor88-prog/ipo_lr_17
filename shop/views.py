from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Product, Category, Manufacture
from users.models import Cart, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


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