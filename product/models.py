from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

from account.models import Client
from product.enums import SellType


class Basemodel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


#Mavsum
class Capsule(Basemodel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='capsule_images')

    @property
    def get_image_url(self):
        return f'http://127.0.0.1:8000/{self.image.url}'

    def __str__(self):
        return self.name


#Tovar partiyasi
class Lookbook(Basemodel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='capsule_images')

    @property
    def get_image_url(self):
        return f'http://127.0.0.1:8000/{self.image.url}'

    def __str__(self):
        return self.name


class LookbookImage(Basemodel):
    lookbook = models.ForeignKey(Lookbook, on_delete=models.CASCADE, related_name='lookbookimage')
    image = models.ImageField(upload_to='lookbook_images')


class LookbookVideo(Basemodel):
    lookbook = models.ForeignKey(Lookbook, on_delete=models.CASCADE, related_name='lookbookvideo')
    video = models.FileField(upload_to='lookbook_videos')


class Category(Basemodel):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='category_images',null=False)
    is_active = models.BooleanField(default=True)

    @property
    def get_image_url(self):
        return f'http://127.0.0.1:8000/{self.image.url}'

    def __str__(self):
        return self.name


class Color(Basemodel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Size(Basemodel):
    size = models.PositiveIntegerField(validators=[MinValueValidator(30), MaxValueValidator(50)])

    def __str__(self):
        return str(self.size)


class MadeType(Basemodel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(Basemodel):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    description = models.TextField(default='')
    price = models.FloatField()

    capsule = models.ForeignKey(Capsule, on_delete=models.CASCADE,related_name='product')
    lookbook = models.ForeignKey(Lookbook, on_delete=models.CASCADE,related_name='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='product')
    color = models.ForeignKey(Color, on_delete=models.CASCADE,related_name='product')
    sell_type = models.CharField(max_length=20, choices=SellType.choices())

    is_main = models.BooleanField(default=False, verbose_name='Asosiy')
    is_new = models.BooleanField(default=False, verbose_name='Yangi')
    is_cheap = models.BooleanField(default=False, verbose_name='Trekotaj')
    is_xit = models.BooleanField(default=False, verbose_name='Xit')

    mades = models.ManyToManyField(MadeType, through='ProductMade', related_name='product')
    sizes = models.ManyToManyField(Size, through='ProductSize', related_name='product')

    is_active = models.BooleanField(default=True)
    # in_discount = models.BooleanField(default=False)
    # discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)


    # @property
    # def is_in_discount(self):
    #     active_discounts = 1
    #     pass
    #
    # @property
    # def which_discount(self):
    #     pass

    # @property
    # def discount_amount(self):
    #     if self.in_discount:
    #         return self.discount.percentage
    #     return 0
    #
    # @property
    # def get_sell_price(self):
    #     discount = self.discount_amount
    #     if discount > 0:
    #         return self.price * (100 - self.discount_amount)
    #     else:
    #         return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Mahsulot narxi 0 dan katta bo`lishi kerak!")


class ProductSize(Basemodel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='productsize')
    size = models.ForeignKey(Size, on_delete=models.CASCADE,related_name='productsize')
    count = models.SmallIntegerField(default=1)


class ProductMade(Basemodel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='productmade')
    made = models.ForeignKey(MadeType, on_delete=models.CASCADE,related_name='productmade')
    amount = models.FloatField(validators=[MinValueValidator(0)])


class ProductImage(Basemodel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='productimage')
    image = models.ImageField(upload_to='product_images')

    @property
    def get_image_url(self):
        return f'http://127.0.0.1:8000/{self.image.url}'






