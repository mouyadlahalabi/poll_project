from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('error-403/', views.error_403, name='error_403'),
    
]