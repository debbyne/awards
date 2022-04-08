from django.db import models
from email.mime import image
from django.contrib.auth.models import User
from unicodedata import name
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
     name=models.CharField(max_length=50, blank=True)
     bio=models.TextField(max_length=400, default="My Bio")
     profile_photo=models.ImageField(upload_to = 'photos/',default="",null=True)
     user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
     email = models.EmailField(null=True)

     def __str__(self):
        return f'{self.user.username} Profile'

     @receiver(post_save, sender=User)
     def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

     @receiver(post_save, sender=User)
     def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

     def save_profile(self):
        self.user

     def delete_profile(self):
        self.delete()

    
     def __str__(self):
        return self.user.username


     @classmethod
     def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

     def __str__(self):
        return f'{self.user.username} Profile'
