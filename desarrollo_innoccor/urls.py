"""
URL configuration for desarrollo_innoccor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#from usuarios.views import HomeView,CustomUserCreateView, CustomUserLoginView, CustomUserLogoutView, CustomPasswordResetView, ResetPasswordView,ResetCompleteView
from usuarios.views import HomeView,CustomUserLoginView,CustomPasswordResetView,ResetPasswordView,ResetCompleteView,PasswordResetDoneView,CustomUserCreateView,UserDetailView, UserUpdateView, UserDeleteView
 

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='inicio'),
    path('registro/', CustomUserCreateView.as_view(), name='registro'),
    path('accounts/profile/', HomeView.as_view(), name='profile'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',ResetPasswordView.as_view(), name='password_reset_confirm'),
    path('reset/done/', ResetCompleteView.as_view(), name='password_reset_complete'),
]

"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='inicio'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('registro/', CustomUserCreateView.as_view(), name='registro'),
    path('user/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('user/update/<str:username>/', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/<pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',ResetPasswordView.as_view(), name='password_reset_confirm'),
    path('reset/done/', ResetCompleteView.as_view(), name='password_reset_complete'),
]

