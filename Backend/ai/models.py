from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class AIConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ai_config')
    summary_length = models.CharField(max_length=20, default='medium') # short, medium, long
    quiz_difficulty = models.CharField(max_length=20, default='medium') # easy, medium, hard

class AIRequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_request')
    endpoint = models.CharField(max_length=50) # chat, summery, quiz ...
    timestamp = models.DateTimeField(auto_now_add=True) # when was the request made
    input_length = models.PositiveIntegerField(default=1)
    output_length = models.PositiveIntegerField(default=1)
    processing_time = models.FloatField(default=1)
    success = models.BooleanField(default=True)
    error_message = models.TextField(null=True, blank=True)

class AIchatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_chats')
    question = models.TextField(default="")
    answer = models.TextField(default="")
    context_source = models.CharField(max_length=50, blank=True, null=True) # source of the context(note, summary)
    context_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Q: " + self.question[:30] + "..." 


