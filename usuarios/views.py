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
from django.middleware.csrf import get_token
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from email.mime.text import MIMEText
import smtplib
import random
import string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.middleware import csrf
from django.middleware.csrf import get_token


User = get_user_model()
#class CustomUserLoginView(View):
 #   template_name = 'usuarios/login.html'
   

     
class TokenView(View):
    def get(self,request):
        try:
            csrf_token = get_token(request)
            return JsonResponse({'csrfToken': csrf_token})
        except Exception as e:
                    # Si ocurre un error, devuelves una respuesta JSON con el mensaje de error
                    error = {'error': str(e)}
                    return JsonResponse(error, status=500)
        
class CustomUserLoginView(LoginView):
    def post(self, request):
            try:   

                try:

                    data = json.loads(request.body)
                    username = data.get('username')
                    password = data.get('password')
                    user = authenticate(username=username, password=password)
                except json.JSONDecodeError:

                    response_data = {
                        'error': 'Datos JSON no válidos',
                        # Otros datos que desees incluir en la respuesta JSON
                    }

                    return JsonResponse(response_data,status=400)
                print('Username:', username)
                print('Password:', password)
                if user is not None:

                    login(request, user)
                    token = default_token_generator.make_token(user)
                    response_data = {
                        'status': 'success',
                        'message': 'Inicio de sesión exitoso',
                        'user_id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'role':user.role,
                        'token_inicio': token
                    }                       
                    return JsonResponse(response_data)
                
                else:

                    response_data = {
                        'message': 'Invalid credentials',
                        # Otros datos que desees incluir en la respuesta JSON
                    }
                    return JsonResponse(response_data,status=401)
                
            except Exception as e:
                    response_data = {
                        'error': str(e),
                        # Otros datos que desees incluir en la respuesta JSON
                    }
                    return JsonResponse(response_data,status=500)

class CustomUserCreateView(CreateView):
    def post(self, request):

        try:

            csrf_token = csrf.get_token(request)

            if request.method == 'POST':
                # Analiza los datos JSON enviados en la solicitud
                try:

                    data = json.loads(request.body)

                except json.JSONDecodeError:
                    response_data = {
                        'error': 'Datos JSON no válidos',
                    }
                    return JsonResponse(response_data,status=400)
                # Crea una instancia del formulario con los datos recibidos
                form = CustomUserCreationForm(data)
                # Realiza la validación del formulario
                if not form.is_valid():
                    # Devuelve una respuesta de error con los errores del formulario
                    response_data = {
                        'error': form.errors,
                        # Otros datos que desees incluir en la respuesta JSON
                    }
                    return JsonResponse(response_data, status=400)
                # Los datos son válidos, continúa con la lógica de registro del usuario
                first_name= data.get('first_name')
                last_name= data.get('last_name')
                username = data.get('username')
                password1 = data.get('password1')
                password2 = data.get('password2')
                email = data.get('email')
                # Validar los datos ingresados
                if not username or not password1 or not email or not password2 or not first_name or not last_name:
                    response_data = {
                        'message': 'First Name,Last Name,Username, Password, and Email are required.'
                        # Otros datos que desees incluir en la respuesta JSON
                    }
                    return JsonResponse(response_data, status=400)
                # Crear el nuevo usuario
                try:
                    user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                    response_data = {
                        'message': 'User registered successfully.'
                    }
                    return JsonResponse({'message': 'User registered successfully.'}, status=201)
                except Exception as e:
                    response_data = {
                        'message': str(e)
                    }
                    return JsonResponse(response_data, status=400)  
                
        except Exception as e:
                    response_data = {
                        'error': str(e)
                    }
                    # Si ocurre un error, devuelves una respuesta JSON con el mensaje de error
                    return JsonResponse(response_data, status=500)  
         
    form_class = CustomUserCreationForm  # El formulario personalizado para el registro de usuarios

class UserDetailView(LoginRequiredMixin,View):
    def get(self, request, username):
        try:
            User = get_user_model()
            try:

                user = User.objects.get(username=username)

                if user.role=="Administrador":
                     users = User.objects.all()
                     user_data = [{'id': user.id, 'username': user.username,'first_name':user.first_name,'last_name':user.last_name, 'email': user.email, 'role':user.role} for user in users]
                     return JsonResponse(user_data, safe=False)
                
                else:
                    response_data = {
                        'message': 'Usuario no cuenta con permisos'
                    }
                    return JsonResponse(response_data, status=400)
                
            except User.DoesNotExist:
                    
                    response_data = {
                        'error': 'User not found'
                    }
                    return JsonResponse(response_data, status=404)
            
        except Exception as e:
                    response_data = {
                        'error': str(e)
                    }
                    return JsonResponse(response_data, status=500)
        
class UserUpdatePersonalView(LoginRequiredMixin, View):

    def post(self, request,username):

        try:

            data = json.loads(request.body)
            user_name = username
            user = User.objects.get(username=user_name)

            if user.role=='Asesor':
                data['role'] = 'Asesor'
            # Crea una instancia del formulario con los datos recibidos
            usuario=user.username
            print(usuario)
            if usuario==data.get('username'):
                 data['username'] = 'userr123'
                 print(user.get_username)
                 print(data)
            form = CustomUserUpdateForm(data)

            #print(data)

            # Realiza la validación del formulario
            if not form.is_valid():
                    response_data = {
                        'error': form.errors
                    }

                    return JsonResponse(response_data, status=400)
                # Devuelve una respuesta de error con los errores del formulario
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
                    response_data = {
                        'status': 'success',
                        'message': 'Actualizacion de datos exitosa',
                        'user_id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'role':user.role
                    }                       
                    return JsonResponse(response_data)
                
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
                    response_data = {
                        'status': 'success',
                        'message': 'Actualizacion de datos exitosa',
                        'user_id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'role':user.role
                    }                       
                    return JsonResponse(response_data)
                
            except User.DoesNotExist:
                    response_data = {
                        'message': 'User not found'
                    }
                    return JsonResponse(response_data, status=400)
            
        except Exception as e:
                    # Si ocurre un error, devuelves una respuesta JSON con el mensaje de error
                    response_data = {
                        'error': str(e)
                    }
                    return JsonResponse(response_data, status=500)                   

class UserUpdateAdminView(LoginRequiredMixin, View):

    def post(self, request,username1,username2):
        try:

            csrf_token = csrf.get_token(request)
            data = json.loads(request.body)
            user_name1 = username1
            user_name2 = username2
            user1 = User.objects.get(username=user_name1)
            user2 = User.objects.get(username=user_name2)
            usuario=user2.username
            if usuario==data.get('username'):
                 data['username'] = 'userr123'
            form = CustomUserUpdateForm(data)
            print(data)
            # Realiza la validación del formulario 
                           
            try:

                if user1.role=='Administrador':
                    if not form.is_valid():
                # Devuelve una respuesta de error con los errores del formulario
                        response_data = {
                        'error': form.errors
                        }
                        return JsonResponse(response_data, status=400)
                    new_first_name=data.get('first_name')
                    new_last_name=data.get('last_name')
                    new_username = data.get('username')
                    new_email = data.get('email')
                    new_role= data.get('role')
                    user2.username = new_username
                    user2.email = new_email
                    user2.first_name=new_first_name
                    user2.last_name=new_last_name
                    user2.role=new_role
                    user2.save()
                    response_data = {
                        'status': 'success',
                        'message': 'Actualizacion de datos exitosa',
                        'user_id': user2.id,
                        'username': user2.username,
                        'first_name': user2.first_name,
                        'last_name': user2.last_name,
                        'email': user2.email,
                        'role':user2.role
                    }                       
                    return JsonResponse(response_data)
                
                else:
                    response_data = {
                        'message': 'Usuario no cuenta con permisos'
                    }
                    return JsonResponse(response_data, status=400) 
                
            except User.DoesNotExist:
                    response_data = {
                        'message': 'User not found'
                    }
                    return JsonResponse(response_data, status=400) 
        except Exception as e:
                    # Si ocurre un error, devuelves una respuesta JSON con el mensaje de error
                    response_data = {
                        'error': str(e)
                    }
                    return JsonResponse(response_data, status=500)                    
        
class UserDeleteView(LoginRequiredMixin, View):  

    def post(self, request, user_name1,user_name2):
        try:

            user1 = User.objects.get(username=user_name1)

            if user1.role=='Administrador':
                user2 = User.objects.get(username=user_name2)
                user2.delete()
                users = User.objects.all()
                user_data = [{'id': user.id, 'username': user.username,'first_name':user.first_name,'last_name':user.last_name, 'email': user.email, 'role':user.role} for user in users]                
                response_data = {
                 'message': 'Usuario eliminado exitosamente.',
                 'users': user_data,
                }
                return JsonResponse(response_data, safe=False)
            
            else:

                response_data = {
                        'message': 'Usuario no cuenta con permisos'
                    }
                
                return JsonResponse(response_data, status=400)
                              
        except User.DoesNotExist:
                
                response_data = {
                        'message': 'User not found'
                    }
                
                return JsonResponse(response_data, status=404) 

class ForgotPasswordView(View):

    def post(self, request,user_name):

        data = json.loads(request.body)
        email = data.get('email')
        print(email)
        # Verificar si el correo electrónico existe en la base de datos
        try:
            user = User.objects.get(username=user_name)
            email_data=user.email 
            print(email_data)
            if email!=email_data:
                print("sisas")
                response_data = {
                        'error': 'El correo electrónico no corresponde con el registrado en la base de datos'
                    }   
                return JsonResponse(response_data, status=400)
        except User.DoesNotExist:
                response_data = {
                        'error': 'El correo electrónico no está registrado'
                    }
                return JsonResponse(response_data, status=400) 
        # Generar el token de reinicio de contraseña
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        characters = string.ascii_letters + string.digits
        verification_code = ''.join(random.choice(characters) for _ in range(6))
        user.verification_code=verification_code
        user.save() 
        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587
        smtp_username = 'juliancho_170799@hotmail.com'        
        smtp_password = 'estefani'
        # Crear el mensaje de correo electrónico
        subject = 'Código de verificación'
        message = f'Hola,\n\nHas solicitado un cambio de contraseña\n\nTu código de verificación es: {verification_code}\n\nGracias.'
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = email
        # Enviar el correo electrónico
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
                response_data = {
                'message': 'Correo electrónico enviado exitosamente',
                'user_id': user.pk,
                'token':token,
                'verification_code': verification_code
    }
            print('Correo electrónico de verificación enviado exitosamente')
     
        except Exception as e:
                response_data = {
                        'Error al enviar el correo electrónico:': str(e)
                    }
                return JsonResponse(response_data, status=500)
        
        return JsonResponse(response_data)

class ResetPasswordView(View):

    def post(self, request, id, token):

        data = json.loads(request.body)

        if request.method == 'POST':

            try:

                print(id)
                uid = id
                token = token
                verification_code = data.get('verification_code')
                new_password = data.get('new_password')

                User = get_user_model()
                user = get_object_or_404(User, pk=uid)
                # Verificar el código de verificación
                if user.verification_code != verification_code:
                    response_data = {
                            'error': 'Código de verificación incorrecto'
                        }
                    return JsonResponse(response_data, status=400)
                # Verificar el token
                if not default_token_generator.check_token(user, token):
                    response_data = {
                            'error': 'Token inválido'
                        }
                    return JsonResponse(response_data, status=400)
                # Restablecer la contraseña
                user.set_password(new_password)
                user.save()
                return JsonResponse({'message': 'Contraseña restablecida exitosamente'})
            
            except Exception as e:  
                response_data = {
                        'Error :': str(e)
                    }
                return JsonResponse(response_data, status=500)    
        
        else:
            return JsonResponse({'error': 'Método no permitido'})