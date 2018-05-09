"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.CharField(max_length=50)
    text = models.TextField(max_length=500)
    time = models.TimeField(auto_now = True)
    def __str__(self):
        return self.caption

# Create your models here.
