from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

User = get_user_model()


class Message(models.Model):
    text = models.CharField(verbose_name='Text', db_index=True, max_length=1024)
    sender = models.ForeignKey(User, related_name='sender', verbose_name='Sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', verbose_name='Receiver', on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return self.text
