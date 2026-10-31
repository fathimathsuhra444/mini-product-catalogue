from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Product, Order, CustomerProfile
from .forms import ProductForm, RegisterForm, CustomerProfileForm


# ==================================================
# CHECK ADMIN USER
# ==================================================

def is_admin(user):
    return user.is_staff


# ==================================================
# HOME PAGE
# ==================================================

def home(request):
    products = Product.objects.all().order_by('-created_at')[:6]

    return render(
        request,
        'catalogue/home.html',
        {'products': products}
    )


# ==================================================
# ABOUT PAGE
# ==================================================

def about(request):
    return render(request, 'catalogue/about.html')


# ==================================================
# PRODUCTS PAGE: SEARCH, FILTER, SORT
# ==================================================

@login_required
def products(request):

    search_query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    subcategory = request.GET.get('subcategory', '').strip()
    price_range = request.GET.get('price_range', '').strip()
    sort = request.GET.get('sort', '').strip()

    product_list = Product.objects.all()

    # Search products
    if search_query:
        product_list = product_list.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__icontains=search_query)
            | Q(subcategory__icontains=search_query)
        )

    # Filter category
    if category:
        product_list = product_list.filter(
            category__iexact=category
        )

    # Filter subcategory
    if subcategory:
        product_list = product_list.filter(
            subcategory__iexact=subcategory
        )

    # Filter price
    if price_range == '0-5000':
        product_list = product_list.filter(price__lt=5000)

    elif price_range == '5000-25000':
        product_list = product_list.filter(
            price__gte=5000,
            price__lte=25000
        )

    elif price_range == '25000-75000':
        product_list = product_list.filter(
            price__gt=25000,
            price__lte=75000
        )

    elif price_range == '75000-plus':
        product_list = product_list.filter(price__gt=75000)

    # Sort products
    if sort == 'price_low':
        product_list = product_list.order_by('price')

    elif sort == 'price_high':
        product_list = product_list.order_by('-price')

    elif sort == 'name':
        product_list = product_list.order_by('name')

    else:
        product_list = product_list.order_by('-created_at')

    context = {
        'products': product_list,
        'selected_category': category,
        'selected_subcategory': subcategory,
        'search_query': search_query,
        'price_range': price_range,
        'sort': sort,
    }

    return render(
        request,
        'catalogue/products.html',
        context
    )


# ==================================================
# ADD PRODUCT: ADMIN ONLY
# ==================================================

@login_required
@user_passes_test(is_admin)
def add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('products')

    else:
        form = ProductForm()

    return render(
        request,
        'catalogue/add_product.html',
        {'form': form}
    )


# ==================================================
# EDIT PRODUCT: ADMIN ONLY
# ==================================================

@login_required
@user_passes_test(is_admin)
def edit_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products')

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'catalogue/edit_product.html',
        {
            'form': form,
            'product': product,
        }
    )


# ==================================================
# DELETE PRODUCT: ADMIN ONLY
# ==================================================

@login_required
@user_passes_test(is_admin)
def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('products')

    return render(
        request,
        'catalogue/delete_product.html',
        {'product': product}
    )


# ==================================================
# USER REGISTRATION
# ==================================================

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


# ==================================================
# SHOPPING CART
# ==================================================

@login_required
def cart_view(request):

    cart = request.session.get('cart', {})

    cart_items = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():

        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = int(quantity)

        except (Product.DoesNotExist, ValueError, TypeError):
            continue

        if quantity < 1:
            continue

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    return render(
        request,
        'catalogue/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


# ==================================================
# ADD PRODUCT TO CART
# ==================================================

@login_required
@require_POST
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    try:
        quantity = int(cart.get(product_id, 0))
    except (ValueError, TypeError):
        quantity = 0

    cart[product_id] = quantity + 1

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(request, 'Product added to cart.')

    return redirect('cart')


# ==================================================
# UPDATE SHOPPING CART
# ==================================================

@login_required
@require_POST
def update_cart(request, product_id):

    cart = request.session.get('cart', {})
    product_id = str(product_id)
    action = request.POST.get('action')

    if product_id in cart:

        try:
            quantity = int(cart[product_id])
        except (ValueError, TypeError):
            quantity = 0

        if action == 'increase':
            cart[product_id] = quantity + 1

        elif action == 'decrease':
            if quantity > 1:
                cart[product_id] = quantity - 1
            else:
                del cart[product_id]

        elif action == 'remove':
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# ==================================================
# CHECKOUT: CASH ON DELIVERY AND UPI QR
# ==================================================

@login_required
def checkout(request):

    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    cart_items = []
    total = Decimal('0.00')

    # Calculate cart total
    for product_id, quantity in cart.items():

        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = int(quantity)

        except (Product.DoesNotExist, ValueError, TypeError):
            continue

        if quantity <= 0:
            continue

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    if not cart_items:
        messages.error(request, 'No valid products found in your cart.')
        return redirect('cart')

    # Process checkout form
    if request.method == 'POST':

        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        payment_method = request.POST.get('payment_method', '').strip()

        # Validate delivery details
        if not full_name or not phone or not address:
            return render(
                request,
                'catalogue/checkout.html',
                {
                    'cart_items': cart_items,
                    'total': total,
                    'error': 'Please fill in all required delivery fields.',
                }
            )

        if not phone.isdigit() or len(phone) != 10:
            return render(
                request,
                'catalogue/checkout.html',
                {
                    'cart_items': cart_items,
                    'total': total,
                    'error': 'Please enter a valid 10-digit phone number.',
                }
            )

        if payment_method not in ['COD', 'UPI']:
            return render(
                request,
                'catalogue/checkout.html',
                {
                    'cart_items': cart_items,
                    'total': total,
                    'error': 'Please select a valid payment method.',
                }
            )

        # ------------------------------------------
        # CASH ON DELIVERY
        # ------------------------------------------

        if payment_method == 'COD':

            try:
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone=phone,
                    email=email,
                    address=address,
                    payment_method='COD',
                    payment_status='Pending',
                    total_amount=total,
                    status='Pending',
                )

                request.session['last_order_id'] = order.id
                request.session.pop('pending_payment_order_id', None)
                request.session['cart'] = {}
                request.session.modified = True

                return redirect('order_success')

            except Exception as e:
                print('COD ORDER ERROR:', repr(e))

                return render(
                    request,
                    'catalogue/checkout.html',
                    {
                        'cart_items': cart_items,
                        'total': total,
                        'error': 'Unable to create your order. Check the terminal.',
                    }
                )

        # ------------------------------------------
        # UPI QR PAYMENT
        # ------------------------------------------

        if payment_method == 'UPI':

            try:
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone=phone,
                    email=email,
                    address=address,
                    payment_method='UPI',
                    payment_status='Pending',
                    total_amount=total,
                    status='Pending',
                )

                request.session['pending_payment_order_id'] = order.id
                request.session.modified = True

                return render(
                    request,
                    'catalogue/qr_payment.html',
                    {
                        'order': order,
                        'total': total,
                    }
                )

            except Exception as e:
                print('UPI QR CHECKOUT ERROR:', repr(e))

                return render(
                    request,
                    'catalogue/checkout.html',
                    {
                        'cart_items': cart_items,
                        'total': total,
                        'error': 'Unable to open the UPI QR page. Check the terminal.',
                    }
                )

    # Display checkout page
    return render(
        request,
        'catalogue/checkout.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


# ==================================================
# VERIFY RAZORPAY PAYMENT
# Kept for compatibility with existing URLs.
# The UPI QR checkout above does not use Razorpay.
# ==================================================

@login_required
@require_POST
def verify_payment(request):

    messages.error(
        request,
        'Razorpay verification is not used by the current UPI QR checkout.'
    )

    return redirect('checkout')


# ==================================================
# ORDER SUCCESS PAGE
# ==================================================

@login_required
def order_success(request):

    order_id = request.session.get('last_order_id')

    if not order_id:
        return redirect('products')

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'catalogue/order_success.html',
        {'order': order}
    )


# ==================================================
# PRODUCT DETAIL PAGE
# ==================================================

def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    return render(
        request,
        'catalogue/product_detail.html',
        {'product': product}
    )


# ==================================================
# CUSTOMER PROFILE
# ==================================================

@login_required
def customer_profile(request):

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = CustomerProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('customer_profile')

    else:
        form = CustomerProfileForm(instance=profile)

    return render(
        request,
        'catalogue/customer_profile.html',
        {'form': form}
    )


# ==================================================
# ORDER HISTORY
# ==================================================

@login_required
def orders(request):

    user_orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_orders = user_orders.count()

    active_orders = user_orders.exclude(
        status__in=['Completed', 'Delivered', 'Cancelled']
    ).count()

    completed_orders = user_orders.filter(
        status__in=['Completed', 'Delivered']
    ).count()

    context = {
        'orders': user_orders,
        'total_orders': total_orders,
        'active_orders': active_orders,
        'completed_orders': completed_orders,
    }

    return render(
        request,
        'catalogue/orders.html',
        context
    )
# ==================================================
# ADD OR REMOVE FAVOURITE PRODUCTS
# ==================================================

@login_required
@require_POST
def toggle_favourite(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    favourites = request.session.get('favourites', [])
    favourites = [str(item) for item in favourites]

    product_id = str(product.id)

    if product_id in favourites:
        favourites.remove(product_id)
        messages.success(request, 'Product removed from favourites.')
    else:
        favourites.append(product_id)
        messages.success(request, 'Product added to favourites.')

    request.session['favourites'] = favourites
    request.session.modified = True

    return redirect(request.POST.get('next', 'products'))


# ==================================================
# CUSTOMER FAVOURITE PRODUCTS PAGE
# ==================================================

@login_required
def favourite_products(request):

    favourites = request.session.get('favourites', [])

    products = Product.objects.filter(
        id__in=favourites
    ).order_by('-created_at')

    return render(
        request,
        'catalogue/favourite_products.html',
        {
            'products': products,
        }
    )
@login_required
@require_POST
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    try:
        quantity = int(cart.get(product_id, 0))
    except (ValueError, TypeError):
        quantity = 0

    cart[product_id] = quantity + 1

    request.session['cart'] = cart
    request.session.modified = True

    if request.POST.get('buy_now') == '1':
        return redirect('checkout')

    messages.success(request, 'Product added to cart.')

    return redirect('cart')
@login_required
@require_POST
def delete_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order.delete()

    messages.success(
        request,
        f"Order #{order_id} deleted successfully."
    )

    return redirect("orders")
def products(request):
    product_list = Product.objects.all()

    category = request.GET.get('category', '').strip()
    subcategory = request.GET.get('subcategory', '').strip()
    query = request.GET.get('q', '').strip()

    if category:
        product_list = product_list.filter(category__iexact=category)

    if subcategory:
        product_list = product_list.filter(subcategory__iexact=subcategory)

    if query:
        product_list = product_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'products': product_list,
        'selected_category': category,
        'selected_subcategory': subcategory,
        'query': query,
    }

    return render(request, 'catalogue/products.html', context)
@login_required
@user_passes_test(is_admin)
def delete_product(request, id):

    if request.method != "POST":
        return redirect("products")

    product = get_object_or_404(Product, id=id)
    product_name = product.name

    product.delete()

    messages.success(
        request,
        f'"{product_name}" was deleted successfully!'
    )

    return redirect("products")
