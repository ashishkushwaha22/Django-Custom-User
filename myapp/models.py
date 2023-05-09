from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

"""
AbstractBaseUser - Class to create a custom User with some added fields.

BaseUserManager - Class to manage our custom user. It provides functions to create user and create superuser

"""
class MyUserManager(BaseUserManager):

    # function to create user 
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(email= self.normalize_email(email), **extra_fields)
        # normalize_email() - Treat 'Example@mail.com' & 'example@mail.com' as a same entity.

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # function to create super user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True')
        
        return self.create_user(email, password, **extra_fields)
    
class MyUser(AbstractBaseUser):

    # Our custom feilds for User.
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=250)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    pancard_number = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    # MAking Django to Use Our defined User Manager for this custom user.
    objects = MyUserManager()

    # making email to use for login instead of username, we can give anyother thing like mobile_number, but it should be unique in DB.
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_lable):
        return True
    
    # defining is_staff property as is_admin (boolean)  - by default False (Line no. 43)
    @property
    def is_staff(self):
        return self.is_admin
    
