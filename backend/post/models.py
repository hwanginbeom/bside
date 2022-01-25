from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        """A string representation of the model."""
        return self.title


class User(AbstractUser):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True)
    nickname = models.CharField(max_length=200, unique=True, null=True)

    def __str__(self):
        """A string representation of the model."""
        return self.email


class Meet(models.Model):
    user_id = models.CharField(max_length=200)
    meet_id = models.CharField(max_length=200)
    meet_title = models.TextField()
    meet_date = models.DateTimeField()
    status = models.CharField(max_length=200)
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
    discussion = models.TextField()
    decisions = models.TextField()
    setting_time = models.IntegerField()
    progress_time = models.IntegerField(null=True)

    def __str__(self):
        """A string representation of the model."""
        return self.agenda_id

class Action(models.Model):
    agenda_id = models.CharField(max_length=200)
    action_id = models.CharField(max_length=200)
    action_title = models.TextField()
    person = models.TextField(null=True)
    dead_line = models.DateTimeField(null=True)

    def __str__(self):
        """A string representation of the model."""
        return self.action_id