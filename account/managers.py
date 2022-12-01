from django.db import models
from .enums import UserRoles
from django.contrib.auth.models import BaseUserManager
from django.contrib import auth
from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, full_name, email, password, **extra_fields):
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(
            phone_number=phone_number,
            full_name=full_name,
            email=email,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, full_name, email, password=None, **extra_fields):
        if email is None:
            raise TypeError('User should have a username')
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(phone_number, full_name, email, password, **extra_fields)

    def create_superuser(self, phone_number, full_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self.create_user(phone_number, full_name, email, password, **extra_fields)


class DirectorsManager(CustomUserManager):
    def get_queryset(self):
        return super(DirectorsManager, self).get_queryset().filter(
            role=UserRoles.director.value)

    def create(self, **kwargs):
        kwargs.update({'role': UserRoles.director.value})
        return super(DirectorsManager, self).create(**kwargs)


class VendorsManager(CustomUserManager):
    def get_queryset(self):
        return super(VendorsManager, self).get_queryset().filter(
            role=UserRoles.vendor.value)

    def create(self, **kwargs):
        kwargs.update({'role': UserRoles.vendor.value})
        return super(VendorsManager, self).create(**kwargs)



class ClientManager(CustomUserManager):
    def get_queryset(self):
        return super(ClientManager, self).get_queryset().filter(
            role=UserRoles.client.value)


class StaffManager(CustomUserManager):
    def get_queryset(self):
        return super(StaffManager, self).get_queryset().filter(
            role__in=(UserRoles.director.value, UserRoles.manager.value,UserRoles.vendor.value,))
