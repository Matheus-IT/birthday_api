from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class AuthManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The email field must be provided'))
        if not password:
            raise ValueError(_('The password field must be provided'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Auth(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    objects = AuthManager()

    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.email


class Member(models.Model):
    name = models.CharField(max_length=50)
    profile_picture = models.ImageField(blank=True, null=True)
    phone_number = models.CharField(max_length=12)
    birth_date = models.DateField()

    def __str__(self) -> str:
        return self.name


class Manager(models.Model):
    member_info = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True)
    auth = models.OneToOneField(Auth, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.member_info.name} - {self.auth.email}'
