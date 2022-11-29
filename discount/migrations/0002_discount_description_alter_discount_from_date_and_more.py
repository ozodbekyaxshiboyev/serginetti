# Generated by Django 4.1.2 on 2022-11-29 12:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_remove_product_discount_remove_product_in_discount'),
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='from_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='percentage',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='discount',
            name='to_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='DiscountItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('all', 'all'), ('category', 'category'), ('product', 'product')], max_length=20)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.discount')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
