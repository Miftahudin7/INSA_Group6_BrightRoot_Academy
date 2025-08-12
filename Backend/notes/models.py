from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import os

# Create your models here.
User = get_user_model()

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#1765f5")

    class Meta:
        unique_together = ('name', 'user')

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField(default="")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
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
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.original_name:
            self.original_name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summeries')
    original_note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True)
    original_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Summary of " + self.original_content.title if self.original_content else self.original_file.original_name

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='quizzes')
    title = models.CharField(max_length=200)
    source_note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, blank=True)
    source_file = models.ForeignKey(UploadedFile, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class QuizQuestion(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple choice Questions'),
        ('SAQ', 'Short Answer Questions'),
        ('TFQ', 'True or False Questions'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    question = models.TextField(default="")
    correct_answer = models.TextField(default="")
    options = models.JSONField(default=list, blank=True) # for MCQ
    explanation = models.TextField(blank=True, null=True)
    points = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question[:50] + "..."

