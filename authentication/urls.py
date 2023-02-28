from django.urls import path
from authentication import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate-account/', views.ActivateAccountView.as_view(), name='activate-account'),
]
