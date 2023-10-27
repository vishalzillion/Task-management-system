from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import timedelta
from django.utils import timezone
import datetime

# Create your models here.
class User(AbstractUser):

    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField(null=True, blank=True)
    email=models.EmailField(unique=True)

    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['username','password']



    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    status = (
        (COMPLETED,'Completed'),
        (PENDING,'Pending')
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField(default=timezone.now() + timedelta(days=7))
    priority = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status =models.CharField(max_length=100,choices= status,default="pending")
    created_at = models.DateTimeField(default=timezone.now())


    created_at_week = models.IntegerField(default=datetime.date.today().isocalendar()[1])

    def __str__(self):
        return self.title
    

  

