from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from .enums import UserRoles
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .managers import DirectorsManager, VendorsManager, ClientManager, CustomUserManager, \
    StaffManager
from .services import location_image, validate_image, custom_validator
from phonenumber_field import modelfields
from rest_framework_simplejwt.tokens import RefreshToken



class User(AbstractUser):
    username = None
    full_name = models.CharField(verbose_name='Fullname', max_length=50,unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = modelfields.PhoneNumberField(unique=True)
    role = models.CharField(max_length=20, choices=UserRoles.choices(),default=UserRoles.client.value)
    image = models.FileField(upload_to=location_image, validators=[validate_image, custom_validator], blank=True, null=True,
                             help_text='Maximum file size allowed is 2Mb')

    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    name_cc = models.CharField(max_length=100, blank=True, null=True)
    floor = models.CharField(max_length=100, blank=True, null=True)

    inn = models.CharField(max_length=9, blank=True, null=True, unique=True)
    company_name = models.CharField(max_length=100, blank=True, null=True,unique=True)
    company_address = models.CharField(max_length=100, blank=True, null=True)
    mail_address = models.CharField(max_length=100, blank=True, null=True)
    contract1 = models.CharField(max_length=100, blank=True, null=True)
    contract2 = models.CharField(max_length=100, blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    account1 = models.CharField(max_length=100, blank=True, null=True)
    account2 = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = ['email','phone_number']


    class Meta:
        constraints = (models.UniqueConstraint(
                name='bitta_direktor',
                fields=['role'],
                condition=models.Q(role=UserRoles.director.value)
            ),
        )

    def clean(self):
        if self.inn:
            accurate: bool = self.inn.isdigit() and len(self.inn) == 9
            if not accurate:
                raise ValueError("Inn xato kiritildi")

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data

    def __str__(self):
        return f"{self.full_name} {self.email}"


class Director(User):
    objects = DirectorsManager()

    class Meta:
        proxy = True



class Vendor(User):
    objects = VendorsManager()

    class Meta:
        proxy = True


class Client(User):
    objects = ClientManager()

    class Meta:
        proxy = True



class Staff(User):
    objects = StaffManager()

    class Meta:
        proxy = True

