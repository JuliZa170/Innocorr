from django.contrib import admin
from django.urls import path
from usuarios.views import CustomUserLoginView,ResetPasswordView,CustomUserCreateView,UserDetailView, UserUpdatePersonalView, UserDeleteView, TokenView,UserUpdateAdminView,UserDeleteView,ForgotPasswordView, TokenView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('registro/', CustomUserCreateView.as_view(), name='registro'),
    path('user_data/<str:username>/', UserDetailView.as_view(), name='user_detail'),
    path('user/update/<str:username>/', UserUpdatePersonalView.as_view(), name='user-update'),
    path('user/<str:username1>/update/<str:username2>/', UserUpdateAdminView.as_view(), name='user-update-admin'),
    path('user/delete/<pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('get-csrf-token/', TokenView.as_view(), name='get-csrf-token'),
    path('forgot-password/<str:user_name>/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<str:id>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('user/<str:user_name1>/delete/<str:user_name2>/', UserDeleteView.as_view(), name='user-delete-admin'),
    path('get-csrf-token/', TokenView.as_view, name='get_csrf_token'),
]

