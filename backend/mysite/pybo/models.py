from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    emoji = models.CharField(max_length=50, null=True, blank=True, default="1")
    join_date = models.DateTimeField(auto_now=True, null=True)

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


class Meet(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_column='id')
    meet_id = models.AutoField(primary_key=True)
    meet_title = models.TextField(null=True)
    meet_date = models.DateTimeField(null=True)
    meet_status = models.CharField(max_length=200, null=True)
    rm_status = models.CharField(max_length=200, null=True)
    participants = models.TextField(null=True)
    goal = models.TextField(null=True)
    last_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        """A string representation of the model."""
        return str(self.meet_id)


class Agenda(models.Model):
    meet_id = models.ForeignKey('Meet', on_delete=models.CASCADE, db_column='meet_id')
    agenda_id = models.AutoField(primary_key=True)
    agenda_title = models.TextField(default='')
    agenda_status = models.CharField(max_length=200, blank=True, default='')
    discussion = models.TextField(blank=True, null=True, default='')
    decisions = models.TextField(blank=True, null=True, default='')
    setting_time = models.IntegerField(blank=True, null=True)
    progress_time = models.TextField(blank=True, null=True, default='')
    start_time = models.TextField(blank=True, null=True, default='')
    order_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """A string representation of the model."""
        return str(self.agenda_id)


class Agenda_progress(models.Model):
    agenda_id = models.ForeignKey('Agenda', on_delete=models.CASCADE, db_column='agenda_id')
    progress_id = models.AutoField(primary_key=True)
    progress_time = models.TextField(blank=True, null=True, default="")


class Action(models.Model):
    agenda_id = models.ForeignKey('Agenda', on_delete=models.CASCADE, db_column='agenda_id')
    action_id = models.AutoField(primary_key=True)
    action_title = models.TextField(blank=True, null=True, default="")
    person = models.TextField(blank=True, null=True, default="")
    dead_line = models.DateTimeField(null=True)

    def __str__(self):
        """A string representation of the model."""
        return str(self.action_id)


class SelfCheck(models.Model):
    meet_id = models.ForeignKey('Meet', on_delete=models.CASCADE, db_column='meet_id')
    check_id = models.AutoField(primary_key=True)
    check1 = models.CharField(max_length=200, blank=True, null=True, default='')
    check2 = models.CharField(max_length=200, blank=True, null=True, default='')
    check3 = models.CharField(max_length=200, blank=True, null=True, default='')
    check4 = models.CharField(max_length=200, blank=True, null=True, default='')
    check5 = models.CharField(max_length=200, blank=True, null=True, default='')
    check6 = models.CharField(max_length=200, blank=True, null=True, default='')
    check7 = models.CharField(max_length=200, blank=True, null=True, default='')
    check8 = models.CharField(max_length=200, blank=True, null=True, default='')
    check9 = models.CharField(max_length=200, blank=True, null=True, default='')
    check10 = models.CharField(max_length=200, blank=True, null=True, default='')

    def __str__(self):
        """A string representation of the model."""
        return str(self.check_id)


class Secession(models.Model):
    email = models.CharField(max_length=200)
    cause = models.CharField(max_length=500, null=True, blank=True)
    reg_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.email)


class Emoji(models.Model):
    emoji_id = models.AutoField(primary_key=True)
    emoji_path = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.emoji_path)
