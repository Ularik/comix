from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )
    username = models.CharField(
        max_length=123
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Дополнительные методы и свойства

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def has_perm(self, perm, obj=None):
        """Does the myuser have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the myuser have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the myuser a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return self.username


class UserCheck(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=123)
    password = models.CharField(max_length=123)
    code = models.IntegerField()
