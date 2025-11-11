from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=False, null=False)

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lifetime_hours = models.IntegerField(default=24)  # время жизни в часах

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=self.lifetime_hours)

    def str(self):
        return self.title

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def str(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')