from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Meet(models.Model):
    email = models.CharField(max_length=200)
    meet_id = models.CharField(max_length=200)
    meet_title = models.TextField()
    meet_date = models.DateTimeField()
    meet_status = models.CharField(max_length=200)
    rm_status = models.CharField(max_length=200)
    participants = models.TextField()
    goal = models.TextField()
    last_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        """A string representation of the model."""
        return self.meet_id


class Agenda(models.Model):
    meet_id = models.CharField(max_length=200)
    agenda_id = models.CharField(max_length=200)
    agenda_title = models.TextField(default='')
    agenda_status = models.CharField(max_length=200)
    discussion = models.TextField(null=True)
    decisions = models.TextField(null=True)
    setting_time = models.IntegerField()
    progress_time = models.IntegerField(null=True)

    def __str__(self):
        """A string representation of the model."""
        return self.agenda_id


class Action(models.Model):
    agenda_id = models.CharField(max_length=200)
    action_id = models.CharField(max_length=200)
    action_title = models.TextField(null=True)
    person = models.TextField(null=True)
    dead_line = models.DateTimeField(null=True)

    def __str__(self):
        """A string representation of the model."""
        return self.action_id


class SelfCheck(models.Model):
    meet_id = models.CharField(max_length=200)
    check_id = models.CharField(max_length=200)
    ownership = models.CharField(max_length=200)
    participation = models.CharField(max_length=200)
    efficiency = models.CharField(max_length=200)
    productivity = models.CharField(max_length=200)

    def __str__(self):
        """A string representation of the model."""
        return self.check_id



#로그인 유저
class UserManager(BaseUserManager):
    def create_user(self, email, name=None, nickname=None, password=None, provider=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            nickname=nickname,
            provider=provider,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.create_user(
            email=email,
            password=password
        )

        user.is_superuser = True
        user.save(using=self.db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True)
    nickname = models.CharField(max_length=200, null=True)
    provider = models.CharField(max_length=200, null=True)
    last_login = models.DateTimeField(null=True)
    img = models.CharField(max_length=500, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """A string representation of the model."""
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

