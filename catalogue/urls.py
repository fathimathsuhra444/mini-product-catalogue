from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views


urlpatterns = [

    # ==========================================
    # HOME AND ABOUT
    # ==========================================

    path('', views.home, name='home'),

    path('about/', views.about, name='about'),


    # ==========================================
    # PRODUCTS
    # ==========================================

    path('products/', views.products, name='products'),

    path('products/add/', views.add_product, name='add_product'),

    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),

    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),

    path('products/<int:id>/', views.product_detail, name='product_detail'),


    # ==========================================
    # USER REGISTRATION
    # ==========================================

    path('register/', views.register, name='register'),


    # ==========================================
    # LOGIN AND LOGOUT
    # ==========================================

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),


    # ==========================================
    # PASSWORD RESET
    # ==========================================

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            success_url='/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/reset/done/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),


    # ==========================================
    # SHOPPING CART
    # ==========================================

    path('cart/', views.cart_view, name='cart'),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/update/<int:product_id>/',
        views.update_cart,
        name='update_cart'
    ),


    # ==========================================
    # CHECKOUT AND PAYMENT
    # ==========================================

    path('checkout/', views.checkout, name='checkout'),

    path(
        'payment/verify/',
        views.verify_payment,
        name='verify_payment'
    ),

    path(
        'order-success/',
        views.order_success,
        name='order_success'
    ),


    # ==========================================
    # CUSTOMER PROFILE AND ORDERS
    # ==========================================

    path(
        'customer-profile/',
        views.customer_profile,
        name='customer_profile'
    ),

    path('orders/', views.orders, name='orders'),
    path(
    'payment/verify/',
    views.verify_payment,
    name='verify_payment'
    ),
    path(
    'qr-payment/',
    TemplateView.as_view(template_name='catalogue/qr_payment.html'),
    name='qr_payment'
    ),
    path(
    'favourites/',
    views.favourite_products,
    name='favourite_products'
    ),

    path(
    'favourites/toggle/<int:product_id>/',
    views.toggle_favourite,
    name='toggle_favourite'
    ),
    path(
    "orders/delete/<int:order_id>/",
    views.delete_order,
    name="delete_order"
    ),
    path(
    "products/delete/<int:id>/",
    views.delete_product,
    name="delete_product"
),

]
