
from django.db import models
from email.mime import image
from django.contrib.auth.models import User
from unicodedata import name
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
import datetime as dt
# Create your models here.

class Profile(models.Model):
     name=models.CharField(max_length=50, blank=True)
     bio=models.TextField(max_length=400, default="My Bio")
     profile_photo=CloudinaryField('image',null = True)
     user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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

class Project(models.Model):
    image = CloudinaryField('image')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', null=True)
    title=models.CharField(max_length=30, blank=True)
    time_posted=models.DateTimeField(auto_now_add=True, null=True)
    description = models.TextField(max_length=1000, null=True)
    url = models.URLField(max_length=100, null=True)
    class Meta:
        ordering = ["-pk"]

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    def __str__(self):
        return self.title

    @classmethod 
    def get_project_by_user(cls, user):
        images = cls.objects.filter(user=user)
        return images
    def update_project(self, title, description,image):
        self.title = title
        self.description = description
        self.image = image
        self.save()

    @classmethod
    def get_all_projects(cls):
        projects = Project.objects.all()
        return projects

    @classmethod
    def search_project_name(cls, search_term):
        images = cls.objects.filter(
        title__icontains=search_term)
        return images
    @classmethod
    def get_project_by_user(cls,user_id):
        projects = Project.objects.filter(user_id=user_id)
        return projects
    def _str_(self):
        return self.user.username

    @classmethod
    def get_single_project(cls, id):
        image = cls.objects.get(id=id)
        return image

    def _str_(self):
        return self.title 


class Rates(models.Model):
    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    design =models.IntegerField(choices=RATE_CHOICES, default=0,blank=False)
    content =models.IntegerField(choices=RATE_CHOICES, default=0,blank=False)
    usability =models.IntegerField(choices=RATE_CHOICES, default=0,blank=False)
    average = models.DecimalField(default=1, blank=False, decimal_places=2, max_digits=40)
    date = models.DateTimeField(auto_now_add =True)
    def __str__(self):
        return f'{self.project.title} ratings'
# class Review(models.Model):
    
#     review = (1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6),(7, 7),(8, 8),(9, 9),(10, 10)
#     design = models.IntegerField(choices=review,blank=True,default=0)
#     usability = models.IntegerField(choices=review, blank=True,default=0)
#     content = models.IntegerField(choices=review, blank=True,default=0)
#     overall_score = models.IntegerField(blank=True,default=0)
#     project = models.ForeignKey(Project,on_delete=models.CASCADE)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.project.title} ratings'
