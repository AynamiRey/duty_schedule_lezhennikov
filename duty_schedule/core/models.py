from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.timezone import now

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    position = models.CharField(max_length=100, blank=True, verbose_name="Должность")
    rank = models.CharField(max_length=100, blank=True, verbose_name="Звание")

    # REQUIRED_FIELDS должен содержать только обязательные поля
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class DutySchedule(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='duties')
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class ChangeLog(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

class RegistrationRequest(models.Model):
    username = models.CharField(max_length=25)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=20, blank=True)
    rank = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

class UserChangeRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255, blank=True)
    new_value = models.CharField(max_length=255, blank=True)
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.field_name} - {self.old_value} -> {self.new_value}"

class ChatMessage(models.Model):
    sender = models.ForeignKey('CustomUser', related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey('CustomUser', related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)  # Добавлено поле для отслеживания прочитанных сообщений

    class Meta:
        ordering = ['timestamp']  # Сортировка по времени по умолчанию

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} - {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Уведомление для {self.user}: {self.message[:20]}"

class Task(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    completed = models.BooleanField(default=False)
    date = models.DateField(default=now)

    def __str__(self):
        return self.text

class WorkAttendance(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=now)
    hours_worked = models.IntegerField(default=8)  # По умолчанию 8 часов (как в форме Т-13)
    is_present = models.BooleanField(default=False)  # Отметка о явке

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.is_present}"