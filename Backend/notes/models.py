from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

SUBJECT_CHOICES = [
    ("Maths", "Maths"),
    ("Physics", "Physics"),
    ("Chemistry", "Chemistry"),
    ("Biology", "Biology"),
    ("English", "English"),
]

GRADE_CHOICES = [
    ("Grade9", "Grade 9"),
    ("Grade10", "Grade 10"),
    ("Grade11", "Grade 11"),
    ("Grade12", "Grade 12"),
]

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default="Maths")
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES, default="Grade9")
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'title', 'grade', 'subject')

    def __str__(self):
        return f"{self.title} ({self.subject}-{self.grade})"

class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summaries')
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='summaries')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Summary for {self.file.title} by {self.user.username}"

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='quizzes')
    questions = models.JSONField()  # Store questions and answers as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Quiz for {self.file.title} by {self.user.username}"

class CommonBook(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES)
    file_url = models.URLField()
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.subject}-{self.grade})"
