from django.contrib.auth import authenticate, login,get_user_model
from django.contrib.auth.views import LoginView, LogoutView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView
from django.views.generic.edit import CreateView
from django.views import View
from django.http import JsonResponse
import json
from django.views.generic import TemplateView,DeleteView
from .forms import CustomUserCreationForm,ResetPasswordForm,CustomUserUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import CustomUser

User = get_user_model()
#class CustomUserLoginView(View):
 #   template_name = 'usuarios/login.html'
   
class HomeView(TemplateView):
    template_name = 'usuarios/inicio.html'


class CustomUserLoginView(LoginView):
    def post(self, request):
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print('Username:', username)
            print('Password:', password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
    template_name = 'usuarios/login.html'  # La plantilla para el formulario de inicio de sesión  
    #success_url = reverse_lazy('inicio')


"""
class CustomUserCreateView(CreateView):
    def post(self, request):
        # Obtener los datos del cuerpo de la solicitud POST
        
        data = json.loads(request.body)
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        
        # Validar los datos ingresados
        if not username or not password1 or not email or not password2:
            return JsonResponse({'message': 'Username, password, and email are required.'}, status=400)

        # Crear el nuevo usuario
        try:
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

        # Enviar una respuesta exitosa
        return JsonResponse({'message': 'User registered successfully.'}, status=201)
    form_class = CustomUserCreationForm  # El formulario personalizado para el registro de usuarios
    template_name = 'usuarios/registro.html'  # La plantilla para el formulario de registro
   # success_url = reverse_lazy('login')  # La URL a la que se redirige después de un registro exitoso

"""

class CustomUserCreateView(CreateView):
    def post(self, request):
        if request.method == 'POST':
            # Analiza los datos JSON enviados en la solicitud
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Datos JSON no válidos'}, status=400)

            # Crea una instancia del formulario con los datos recibidos
            form = CustomUserCreationForm(data)

            # Realiza la validación del formulario
            if not form.is_valid():
                # Devuelve una respuesta de error con los errores del formulario
                return JsonResponse({'error': form.errors}, status=400)

            # Los datos son válidos, continúa con la lógica de registro del usuario
            first_name= data.get('first_name')
            last_name= data.get('last_name')
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')
            email = data.get('email')

            
            # Validar los datos ingresados
            if not username or not password1 or not email or not password2:
                return JsonResponse({'message': 'Username, password, and email are required.'}, status=400)

            # Crear el nuevo usuario
            try:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=400)

            return JsonResponse({'message': 'User registered successfully.'}, status=201)
    form_class = CustomUserCreationForm  # El formulario personalizado para el registro de usuarios
    template_name = 'usuarios/registro.html'  # La plantilla para el formulario de registro

class UserDetailView(LoginRequiredMixin,View):
    def get(self, request, username):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
            return JsonResponse(user_data, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

class UserUpdateView(LoginRequiredMixin, View):
    def post(self, request,username):
        data = json.loads(request.body)
        print(data)
        user_name = username
        print(username)
        user = User.objects.get(username=user_name)
        if user.role=='Asesor':
            data['role'] = 'Asesor'
        # Crea una instancia del formulario con los datos recibidos
        form = CustomUserUpdateForm(data)
        print(data)
        # Realiza la validación del formulario
        if not form.is_valid():
            # Devuelve una respuesta de error con los errores del formulario
            return JsonResponse({'error': form.errors}, status=400)
        try:
            if user.role=='Administrador':
                print("admin")
                new_first_name=data.get('first_name')
                new_last_name=data.get('last_name')
                new_username = data.get('username')
                new_email = data.get('email')
                new_role= data.get('role')
                user.username = new_username
                user.email = new_email
                user.first_name=new_first_name
                user.last_name=new_last_name
                user.role=new_role
                user.save()
                return JsonResponse({'message': 'User data updated successfully'})
            elif user.role=='Asesor':  
                print("asesor")
                new_first_name=data.get('first_name')
                new_last_name=data.get('last_name')
                new_username = data.get('username')
                new_email = data.get('email')
                user.username = new_username
                user.email = new_email
                user.first_name=new_first_name
                user.last_name=new_last_name
                user.save()                     
                return JsonResponse({'message': 'User data updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'})

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser

    def form_valid(self, form):
  # Verificar si el usuario actual tiene permiso para eliminar
        if self.request.user.role == 'Administrador':
            print("sisas")
            response = super().form_valid(form)
            return JsonResponse({'message': 'El usuario ha sido eliminado correctamente'})
        else:
            return JsonResponse({'message': 'No tienes permiso para eliminar usuarios'}, status=403)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'usuarios/password_reset.html'
    email_template_name = 'usuarios/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(PasswordResetView):
    template_name = 'usuarios/password_reset_done.html'  # La plantilla para el formulario de inicio de sesión

class ResetCompleteView(TemplateView):
    template_name = 'usuarios/password_reset_complete.html'

class ResetPasswordView(PasswordResetConfirmView):
    template_name = 'usuarios/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
"""
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView,PasswordResetView,PasswordResetCompleteView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetConfirmView
from django.views.generic.edit import FormView
from .forms import ResetPasswordForm
# Create your views here.

class ResetPasswordView(PasswordResetConfirmView):
    template_name = 'usuarios/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


class HomeView(TemplateView):
    template_name = 'usuarios/inicio.html'

class CustomUserLoginView(LoginView):
    template_name = 'usuarios/login.html'  # La plantilla para el formulario de inicio de sesión  
    success_url = reverse_lazy('inicio')

class CustomUserLogoutView(LogoutView):
    next_page = 'usuarios/inicio.html'  # La página a la que se redirige después de cerrar sesión

class CustomPasswordResetView(PasswordResetView):
    template_name = 'usuarios/password_reset.html'
    email_template_name = 'usuarios/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')



class PasswordResetDoneView(PasswordResetView):
    template_name = 'usuarios/password_reset_done.html'  # La plantilla para el formulario de inicio de sesión

class ResetCompleteView(TemplateView):
    template_name = 'usuarios/password_reset_complete.html'

"""