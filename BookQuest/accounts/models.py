from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=10,unique=True)
    class Meta:
        db_table = "USER"

# ! For CustomUser Model to change username field or else
# from django.contrib.auth.base_user import BaseUserManager
# class UserManager(BaseUserManager):

#     def create_user(self, username, password, **extra_fields):
#         if not username:
#             raise ValueError("Username. is reqired")
        
#         extra_fields['email'] = self.normalize_email(extra_fields['email'])
#         user = self.model(username=username,**extra_fields)
#         user.set_password(password)
#         user.save(using = self.db)
#         return user

#     def create_superuser(self, username, password, **extra_fields):
#         extra_fields.setdefault("is_active",True)
#         extra_fields.setdefault("is_staff",True)
#         extra_fields.setdefault("is_superuser",True)

#         return self.create_user(username, password, **extra_fields)