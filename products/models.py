import os

from django.db import models

from authentication.models import User


def get_product_3d_asset_path(instance, filename):
    return os.path.join('bundles', str(instance.bundle.pk), 'assets', filename)


def get_product_image_path(instance, filename):
    return os.path.join('bundles', str(instance.bundle.pk), 'images', filename)


class Bundle(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='bundles', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bundles'

    def __str__(self):
        return self.name


class Product(models.Model):
    bundle = models.ForeignKey(Bundle, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_product_image_path, blank=True, null=True)
    asset = models.FileField(
        upload_to=get_product_3d_asset_path,
        blank=True,
        null=True,
        max_length=126,
        verbose_name='3D assets',
    )

    class Meta:
        db_table = 'products'
        constraints = [
            models.UniqueConstraint(
                fields=['bundle', 'name'],
                name='unique_bundle_product',
            )
        ]

    def __str__(self):
        return self.name
