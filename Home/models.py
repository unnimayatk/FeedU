from django.db import models
from django.utils import timezone
import random
from django.contrib.auth. models import User


class FoodMenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=25,
        choices=(("Food", "Food"), ("Snakes", "Snakes"), ("Beverages", "Beverages"), ("Diet_Food", "Diet_Food"))
    )
    image = models.ImageField(upload_to='menu_images/')
    available = models.BooleanField(default=True)
    rate = models.FloatField()
    discount_rate = models.FloatField( null=True, blank=True)
    offer = models.BooleanField(default=False, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        if self.discount_rate:
            return self.rate - (self.rate * self.discount_rate / 100)
        return self.rate


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, default="pending")
    payment_status = models.CharField(max_length=20, default="pending")

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        while True:
            random_number = random.randint(10000, 999999)
            order_number = f"PRO-{random_number}"
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    @classmethod
    def get_or_create_pending_order(cls,request):
        order = cls.objects.filter(order_status="pending").first()
        if not order:
            order = cls.objects.create(order_status="pending", user=request.user)
        return order

    def update_total_amount(self):
        self.total_amount = sum(item.total_price for item in self.order_items.all())
        self.save()


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
    product = models.ForeignKey(FoodMenuItem, on_delete=models.CASCADE, related_name='foods')
    quantity = models.FloatField(default=1)
    total_price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.rate
        super().save(*args, **kwargs)

    @classmethod
    def add_or_update_item(cls, order, product_id, quantity=1):
        try:
            # Check if item already exists in the order
            item = cls.objects.get(order=order, product_id=product_id)
            item.quantity += quantity
            item.save()
        except cls.DoesNotExist:
            # Create a new order item if it doesn't exist
            product = FoodMenuItem.objects.get(id=product_id)
            item = cls.objects.create(order=order, product=product, quantity=quantity, total_price=product.rate * quantity)
        # Update order total amount after adding/updating item
        order.update_total_amount()
        return item


class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='delivery')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    order_status = models.CharField(max_length=20, default="Order Received")
    estimated_time = models.TimeField(null=True, blank=True)
    delivery_status = models.BooleanField(default=False)
    ordered_time = models.DateTimeField(auto_now_add=True)
    delivery_time = models.CharField(null=True, blank=True, max_length=20)
    rating  = models.IntegerField(null=True, blank=True)





