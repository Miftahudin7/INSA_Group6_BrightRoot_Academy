from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    dark_mode = models.BooleanField(default=False)
    study_goal = models.CharField(max_length=200, blank=True)
    last_active = models.DateTimeField(default=timezone.now)

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save()

class StudyStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)
     

