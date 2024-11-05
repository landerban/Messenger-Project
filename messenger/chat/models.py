from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from cryptography.fernet import Fernet

fernet = Fernet(settings.FERNET_KEY)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_id=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not user_id:
            raise ValueError("The User ID field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, user_id=user_id, **extra_fields)
        user.set_first_name(first_name)
        user.set_last_name(last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, user_id=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, user_id=user_id, first_name=first_name, last_name=last_name, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=100, unique=True)
    first_name_encrypted = models.BinaryField()
    last_name_encrypted = models.BinaryField()
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id']

    def set_first_name(self, first_name):
        self.first_name_encrypted = fernet.encrypt(first_name.encode())

    @property
    def first_name(self):
        return fernet.decrypt(self.first_name_encrypted).decode()

    def set_last_name(self, last_name):
        self.last_name_encrypted = fernet.encrypt(last_name.encode())

    @property
    def last_name(self):
        return fernet.decrypt(self.last_name_encrypted).decode()

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name="received_messages", on_delete=models.CASCADE)
    content_encrypted = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def set_content(self, content):
        self.content_encrypted = fernet.encrypt(content.encode())

    def get_content(self):
        return fernet.decrypt(self.content_encrypted).decode()