from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    User,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_("The email field must be provided"))
        if not password:
            raise ValueError(_("The password field must be provided"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    def __str__(self) -> str:
        return self.email


class Member(models.Model):
    name = models.CharField(max_length=50)
    profile_picture = models.ImageField(blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    birth_date = models.DateField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Manager(models.Model):
    member_info = models.OneToOneField(
        Member, on_delete=models.SET_NULL, blank=True, null=True
    )
    auth = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.member_info:
            return f"{self.member_info.name} - {self.auth.email}"
        return self.auth.email


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
