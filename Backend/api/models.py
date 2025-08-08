from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    dark_mode = models.BooleanField(default=False)
    study_goal = models.CharField(max_length=200, blank=True, null=True)
    streak_count = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#3774d5")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.CharField(max_length=200, blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded')
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.original_name
    
class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summeries')
    original_content = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True)
    original_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Summary of " + self.original_content.title if self.original_content else self.original_file.original_name

class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    next_review_date = models.DateTimeField(default=timezone.now)
    ease_factor = models.FloatField(default=3) # difficulty rating
    repetition_number = models.IntegerField(default=0) # successful
    interval = models.IntegerField(default=1)

    def __str__(self):
        return self.question[:50] + "..."

# last check
class Quiz(models.Model):
    



