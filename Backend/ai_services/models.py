from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AIRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_requests')
    request_type = models.CharField(max_length=50)  # 'summary' or 'quiz'
    content = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.request_type} request by {self.user.username}"
