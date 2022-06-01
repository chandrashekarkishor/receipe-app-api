"""
Database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

# Create your models here.


class UserManager(BaseUserManager):
    """
    Manage users
    """
    def create_user(self, email, password=None, **kwargs):
        """
        Create, Save and return user
        :param email:
        :param password:
        :param kwargs:
        :return:
        """
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **kwargs)
        # model in base user manager will uses User model class
        # as it is assigned as model in base user manager
        user.set_password(password)
        user.save(using=self._db)  # self._db is to support muliple dB
        return user

    def create_superuser(self, email, password):
        """
        Create save and return Super user
        :param email:
        :param password:
        :return:
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User in the system
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # Assigne Manager

    USERNAME_FIELD = 'email'
