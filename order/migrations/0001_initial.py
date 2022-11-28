# Generated by Django 4.1.2 on 2022-11-25 06:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('wait_pay', 'wait_pay'), ('cancelled', 'cancelled'), ('paid', 'paid')], default='wait_pay', max_length=20)),
                ('total_price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_paid', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='account.client')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('total_price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='account.client')),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('total_price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlistitem', to='product.product')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlistitem', to='order.wishlist')),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItemSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('productsize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlistitemsize', to='product.productsize')),
                ('wishlistitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlistitemsize', to='order.wishlistitem')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('orderitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitemsize', to='order.orderitem')),
                ('productsize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitemsize', to='product.productsize')),
            ],
        ),
    ]