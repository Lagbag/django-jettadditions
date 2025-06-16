from django.urls import path
from django_jettadditions import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('change_password/', views.change_password, name='change_password'),
    path('validate/', views.validate_view, name='validate'),
    path('dashboard/', views.admin_panel, name='admin_panel'),
    path('dashboard/register/', views.register_user, name='register_user'),
    path('dashboard/update/<int:user_id>/', views.update_user, name='update_user'),
]