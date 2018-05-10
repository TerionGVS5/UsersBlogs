"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail

class Post(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.CharField(max_length=50)
    text = models.TextField(max_length=500)
    time = models.TimeField(auto_now = True)
    def __str__(self):
        return self.caption
    # Отправка письма при добавлении поста, если указан email
    def save(self, *args, **kwargs):
        subs = Subscription.objects.all().filter(blogger=self.owner).values('user')
        users = User.objects.all().filter(pk__in=subs)
        super(Post, self).save(*args, **kwargs)
        for u in users:
            if u.email:
                message = 'Here new post! http://localhost:8000/private_office/post_detail/{}/'.format(self.pk)
                send_mail(
                   'New post!',
                   message,
                   'BlogsUsers@example.com',
                    [u.email],
                fail_silently=False,
                )

class Subscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blogger = models.ForeignKey(User,on_delete=models.CASCADE, related_name='+')

class Reading(models.Model):
    reader = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
# Create your models here.
