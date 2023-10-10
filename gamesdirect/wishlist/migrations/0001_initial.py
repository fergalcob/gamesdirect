# Generated by Django 4.2 on 2023-10-10 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store_pages', '0002_delete_wishlist'),
    ]

    operations = [
       migrations.SeparateDatabaseAndState(
        state_operations=[
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wishlist_items', models.ManyToManyField(to='store_pages.game')),
                    ],
                ),
            ],
            # Table already exists. See catalog/migrations/0003_delete_product.py
           database_operations=[],
         ),
     ]