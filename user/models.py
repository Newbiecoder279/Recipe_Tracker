from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class CreateUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    

class NewRecipe(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    title = models. CharField(max_length=250)
    picture = models.ImageField(upload_to='recipe_images/')
    ingrediants = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    