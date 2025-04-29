from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self,first_name,last_name, email,user_role='customer', password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name,last_name=last_name,email=email,user_role=user_role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,last_name, email,user_role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(first_name,last_name,email,user_role, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    choices = [('manager', 'Manager'), ('employee', 'Employee'), ('inventory_manager', 'Inventory Manager'), ('driver', 'Driver'),('customer', 'Customer')]
    user_role = models.CharField(max_length=20, choices=choices)

    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','user_role']
    
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=100)
    governorate = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_profile.png')

    def __str__(self):
        return self.user.email

