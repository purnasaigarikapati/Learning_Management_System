from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('INSTRUCTOR', 'Instructor'),
        ('STUDENT', 'Student'),
    )
    user_id=models.AutoField(primary_key=True)
    name=models.CharField(unique=True,max_length=225)
    password = models.CharField(max_length=16)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=100)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='STUDENT'
    )



