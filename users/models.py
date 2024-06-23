from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=15, unique=True, verbose_name='phone_number')
    username = models.CharField(max_length=255, verbose_name='username')
    is_active = models.BooleanField(default=True, verbose_name='is_active')
    is_staff = models.BooleanField(default=False, verbose_name='is_staff')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

