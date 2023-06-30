from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    # Agrega campos adicionales aquí si es necesario
    role = models.CharField(max_length=55, default='Asesor')