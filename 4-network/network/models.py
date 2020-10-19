from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')

    def __str__(self):
        return f'Profile: {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    
    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            #  "user": self.user,
            "content": self.content,
            "date_posted": self.date_posted,
            "likes": randint(0, 100)
        }