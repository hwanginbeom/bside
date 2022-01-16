from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        """A string representation of the model."""
        return self.title

class Meet_infor(models.Model):
    meet_number = models.CharField(max_length=200)
    meet_name = models.CharField(max_length=200)
    meet_agenda1 = models.TextField()
    meet_agenda2 = models.TextField()
    meet_agenda3 = models.TextField()
    meet_agenda4 = models.TextField()
    meet_agenda5 = models.TextField()
    total_time = models.CharField(max_length=200)
    next_time = models.CharField(max_length=200)
    meet_record = models.TextField()

    def __str__(self):
        """A string representation of the model."""
        return self.meet_number