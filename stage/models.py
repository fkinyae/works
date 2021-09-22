from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    bio=models.CharField(max_length=500,null=True,blank=True)
    profile_pic=models.ImageField(upload_to="profile_pics/",default='default.png')
    twitter_url=models.CharField(max_length=500,null=True,blank=True)

    
    def __str__(self):
        return str(self.user)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
        
class Project(models.Model):
    title=models.CharField(max_length=200)
    url=models.URLField(max_length=200)
    description=models.TextField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='projects/photos/',default='default.png')
    date=models.DateTimeField(auto_now_add=True,blank=True)
    
    def __str__(self):
        return str(self.title)
    
    def delete_project(self):
        self.delete()
        
    def save_project(self):
        self.save()    
        
    @classmethod
    def search_project(cls, search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects
    
    @classmethod
    def all_projects(cls):
        return cls.objects.all()    
    
class Rate(models.Model):  
    ratings= (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
    (8, "8"),
    (9, "9"),
    (10, "10"),
    )
    design=models.IntegerField(choices=ratings,default=0,blank=True)
    usability=models.IntegerField(choices=ratings,default=0,blank=True)
    content=models.IntegerField(choices=ratings,default=0,blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    project=models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    
    def save_rating(self):
        self.save()   
    
    @classmethod  
    def get_ratings(cls):    
        ratings=Rate.objects.all()
        return ratings
    
    def __str__(self):
        return f'{self.project} Rate'


          
    
   

