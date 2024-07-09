from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# from django.contrib.auth.models import BaseUserManager


class User(AbstractUser):
    username=models.CharField(max_length=30,unique=True)
    email = models.EmailField('email address',unique=True)
    phone_no = models.CharField(max_length=10)
    password = models.CharField(max_length=200)
    confirm_password = models.CharField(max_length=50)  
    created_at = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(default='default.jpg', upload_to='profile_pics',null=True )
    updated_at = models.DateTimeField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(User, self).save(*args, **kwargs)



class CaptchaData(models.Model):
    captcha_text = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
