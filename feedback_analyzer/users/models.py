from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import UniqueEmailValidator, EmailFormatValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, password=None):
    #     user = self.create_user(email, password=password)
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user

class Users(AbstractBaseUser):
    class Meta:
        app_label = 'users'

    email = models.EmailField(validators=[UniqueEmailValidator(), EmailFormatValidator()],unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    #def has_module_perms(self, app_label):
    #    return True
