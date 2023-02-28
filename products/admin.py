from django.contrib import admin

from products.models import Product, Bundle


@admin.register(Bundle)
class AdminBundle(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    list_filter = ('name', 'user')


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('id', 'name', 'bundle', 'user')
    list_filter = ('name', 'bundle')

    @admin.display
    def user(self, object):
        return object.bundle.user.email
