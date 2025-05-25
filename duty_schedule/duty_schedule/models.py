from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=100, blank=True)
    rank = models.CharField(max_length=100, blank=True)

class DutySchedule(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()

class ChangeLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class RegistrationRequest(models.Model):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)