from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    bio=models.CharField(max_length=500,null=True,blank=True)
    profile_pic=models.ImageField(upload_to="profile_pics/",null=True,blank=True)
    twitter_url=models.CharField(max_length=500,null=True,blank=True)

    
    def __str__(self):
        return str(self.user)


    
    

