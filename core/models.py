import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
class Customer(models.Model):
    """Customer Model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="customers/avatars", blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payment_method_id = models.CharField(max_length=255, blank=True)
    stripe_card_last = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()
    
class Category(models.Model):
    """Category Model"""
    slug = models.SlugField(blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)

class Job(models.Model):
    """Job Model"""
    QUANTITY_SMALL = "small"
    QUANTITY_MEDIUM = "medium"
    QUANTITY_LARGE = "large"

    QUANTITY_CHOICES = (
        (QUANTITY_SMALL, "Small"),
        (QUANTITY_MEDIUM, "Medium"),
        (QUANTITY_LARGE, "Large")
    )

    STATUS_CREATE = "creating"
    STATUS_PICKUP = "pickup"
    STATUS_DROP = "droping"
    STATUS_COMPLETE = "complete"
    STATUS_CANCEL = "canceled"
    STATUS_PAYMENT = "payment"

    STATUS_CHOICES = (
        (STATUS_CREATE, "Creating"),
        (STATUS_PICKUP, "Pickup"),
        (STATUS_DROP, "Droping"),
        (STATUS_PAYMENT, "Payment"),
        (STATUS_COMPLETE, "Complete"),
        (STATUS_CANCEL, "Canceled"),
        
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.CharField(max_length=20, choices=QUANTITY_CHOICES, default=QUANTITY_MEDIUM)
    image = models.ImageField(upload_to="job/images/")
    created_on = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATE)
    
    pickup_address = models.CharField(max_length=256)
    pickup_name = models.CharField(max_length=255)
    pickup_lat = models.FloatField(blank=True, null=True)
    pickup_lng = models.FloatField(blank=True, null=True)
    pickup_phone = models.CharField(max_length=20)
    
    
    drop_address = models.CharField(max_length=256)
    drop_name = models.CharField(max_length=255)
    drop_lat = models.FloatField(blank=True, null=True)
    drop_lng = models.FloatField(blank=True, null=True)
    drop_phone = models.CharField(max_length=20)
    

    def __str__(self):
        return str(self.id)