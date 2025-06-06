from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,  PermissionsMixin
import uuid
from . manager import CustomUserManager
# Create your models here.






class User(AbstractBaseUser , PermissionsMixin):
    id = models.UUIDField(primary_key=True , default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True,db_index=True)
    full_name = models.CharField(max_length=55)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
