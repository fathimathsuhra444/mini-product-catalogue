from django.db import models
from django.contrib.auth.models import User


# ==========================================
# PRODUCT MODEL
# ==========================================

class Product(models.Model):

    # Main categories
    CATEGORY_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Smartphone', 'Smartphone'),
        ('Headphones', 'Headphones'),
        ('Tablets','Tablets'),
        ('Gaming','Gaming'),
        ('Wearables','Wearables')
    ]

    # Product subcategories
    SUBCATEGORY_CHOICES = [

        # Laptop subcategories
        ('Gaming Laptop', 'Gaming Laptop'),
        ('Business Laptop', 'Business Laptop'),
        ('Student Laptop', 'Student Laptop'),
        ('Personal Laptop', 'Personal Laptop'),
        ('Creator Laptop', 'Creator Laptop'),
        ('Ultrabook', 'Ultrabook'),

        # Smartphone subcategories
        ('Android Smartphone', 'Android Smartphone'),
        ('iPhone', 'iPhone'),
        ('Camera Smartphone', 'Camera Smartphone'),
        ('Gaming Smartphone', 'Gaming Smartphone'),
        ('Budget Smartphone', 'Budget Smartphone'),
        ('Premium Smartphone', 'Premium Smartphone'),

        # Headphone subcategories
        ('Wireless Headphones', 'Wireless Headphones'),
        ('Wired Headphones', 'Wired Headphones'),
        (
            'Noise-Cancelling Headphones',
            'Noise-Cancelling Headphones'
        ),
        ('Gaming Headphones', 'Gaming Headphones'),
        ('Earbuds', 'Earbuds'),

        # Tablets subcategories
        ('Android Tablets', 'Android Tablets'),
        ('iPads', 'iPads'),
        ('Gaming Tablets', 'Gaming Tablets'),
        ('Student Tablets', 'Student Tablets'),
        ('Premium Tablets', 'Premium Tablets'),

        # Gaming subcategories
        ('Gaming Consoles', 'Gaming Consoles'),
        ('Gaming Keyboards', 'Gaming Keyboards'),
        ('Gaming Mouse', 'Gaming Mouse'),
        ('Gaming Headsets', 'Gaming Headsets'),
        ('Gaming Controllers', 'Gaming Controllers'),

        # Wearables subcategories
        ('Smartwatches', 'Smartwatches'),
        ('Fitness Bands', 'Fitness Bands'),
        ('Smart Rings', 'Smart Rings'),
        ('GPS Watches', 'GPS Watches'),
        ('Premium Smartwatches', 'Premium Smartwatches'),
    ]

    # Product information
    name = models.CharField(max_length=200)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    subcategory = models.CharField(
        max_length=100,
        choices=SUBCATEGORY_CHOICES,
        blank=True
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# ==========================================
# ORDER MODEL
# ==========================================

class Order(models.Model):

    # Available payment methods
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
    ]

    # Available order statuses
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    # Customer account
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    # Customer information
    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=10)

    email = models.EmailField(blank=True)

    address = models.TextField(max_length=500)

    # Payment information
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    # Total order amount
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # Order status
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # Order date and time
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


# ==========================================
# CUSTOMER PROFILE MODEL
# ==========================================

class CustomerProfile(models.Model):

    # Connect one profile to one customer account
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )

    # Customer contact information
    phone = models.CharField(
        max_length=15,
        blank=True
    )

    # Customer address
    address = models.TextField(
        blank=True
    )

    # Customer city
    city = models.CharField(
        max_length=100,
        blank=True
    )

    # Customer PIN code
    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - Profile"
# ==========================================
# ORDER MODEL
# ==========================================

class Order(models.Model):

    # Available payment methods
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI Online Payment'),
    ]

    # Available order statuses
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    # Payment statuses
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    # Customer account
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    # Customer information
    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=10)

    email = models.EmailField(blank=True)

    address = models.TextField(max_length=500)

    # Payment method
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    # Payment status
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

    # Razorpay order ID
    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True
    )

    # Razorpay payment ID
    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True
    )

    # Total order amount
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # Order status
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # Order date and time
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"