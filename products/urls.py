from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('bundles/', views.BundleListView.as_view(), name='bundle-list'),
    path('bundles/create/', views.BundleCreateView.as_view(), name='bundle-create'),
    path('bundles/<int:bundle_id>/', views.BundleDetailView.as_view(), name='bundle-detail'),
    path('bundles/<int:bundle_id>/update/', views.BundleUpdateView.as_view(), name='bundle-update'),
    path('bundles/<int:bundle_id>/delete/', views.BundleDeleteView.as_view(), name='bundle-delete'),

    path('bundles/<int:bundle_id>/products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:product_id>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('products/<int:product_id>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    # path('bundles/create/', views.BundleListView.as_view(), name='bundle-create'),
    # path('bundles/<int:bundle_id>/update/', views.BundleListView.as_view(), name='bundle-update'),
    # path('bundles/<int:bundle_id>/delete/', views.BundleListView.as_view(), name='bundle-delete'),
]
