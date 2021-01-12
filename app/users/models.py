from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, blank=False, verbose_name='Email Address')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'