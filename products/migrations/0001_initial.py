# Generated by Django 4.1.7 on 2023-02-21 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bundles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bundles',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to=products.models.get_product_image_path)),
                ('asset', models.FileField(blank=True, max_length=126, null=True, upload_to=products.models.get_product_3d_asset_path, verbose_name='3D assets')),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.bundle')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('bundle', 'name'), name='unique_bundle_product'),
        ),
    ]
