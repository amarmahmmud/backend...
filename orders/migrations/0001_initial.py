# Generated by Django 5.1.4 on 2024-12-20 05:55

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('PR', 'Processing'), ('SH', 'Shipped'), ('DE', 'Delivered'), ('CA', 'Cancelled'), ('RF', 'Refunded')], default='PE', max_length=2)),
                ('payment_method', models.CharField(choices=[('CC', 'Credit Card'), ('DC', 'Debit Card'), ('PP', 'PayPal'), ('ST', 'Stripe'), ('CD', 'Cash on Delivery')], default='CC', max_length=2)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shipping_address', models.TextField()),
                ('shipping_method', models.CharField(blank=True, max_length=100)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('price_at_time', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='products.product')),
            ],
        ),
    ]
