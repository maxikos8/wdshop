from django.shortcuts import render, get_object_or_404 , redirect
from .models import Category, Product, Order, OrderItem  # ← вот тут добавил OrderItem!
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    categories = Category.objects.all()
    bestsellers = Product.objects.filter(is_bestseller=True, available=True)
    return render(request, 'index.html', {
        'categories': categories,
        'bestsellers': bestsellers
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })
        cart_total += total

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'cart.html', context)

def cart_update(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        # Изменение количества
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity < 1:
                        cart.pop(product_id, None)
                    else:
                        cart[product_id] = quantity
                except ValueError:
                    continue
        # Удаление
        if 'remove' in request.POST:
            product_id = request.POST['remove']
            cart.pop(product_id, None)
        request.session['cart'] = cart
    return redirect('cart')

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(product.pk)] = cart.get(str(product.pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def api_add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        qty = int(request.POST.get("quantity", 1))
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + qty  # ← ТЕПЕРЬ + qty
        request.session['cart'] = cart
        count = sum(cart.values())
        return JsonResponse({'ok': True, 'cart_count': count})
    return JsonResponse({'ok': False})

# Checkout view пока может быть-заглушкой, обработку обсудим отдельно
def checkout_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(pk__in=cart.keys())
    cart_items = []
    cart_total = 0
    for p in products:
        qty = cart.get(str(p.pk), 0)
        total = p.price * qty
        cart_items.append({'product': p, 'quantity': qty, 'total': total})
        cart_total += total

    if request.method == "POST":
        delivery = request.POST.get('delivery')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        comment = request.POST.get('comment')
        order = Order.objects.create(
            name=name,
            phone=phone,
            email=email,
            delivery=delivery,
            address=address,
            comment=comment
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
        # Очищаем корзину
        request.session['cart'] = {}
        return render(request, "order_success.html", {"order": order})

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "cart_total": cart_total
    })
