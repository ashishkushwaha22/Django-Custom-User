from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(email= self.normalize_email(email), **extra_fields)
        # Anamika@mail.com
        # anamika@mail.com

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True')
        
        return self.create_user(email, password, **extra_fields)
    
class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=250)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    pancard_number = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_lable):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
