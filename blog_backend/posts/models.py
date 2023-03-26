from django.db import models
from django.urls import reverse
from django.db.models.deletion import CASCADE
from datetime import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
#from django.contrib.auth.models import User

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
       Token.objects.create(user=instance)

       
class Coustomer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    #moderators = models.ForeignKey(User, related_name="moderators", null=True, on_delete=CASCADE) 
    def __str__(self):
        return self.name

        

class Post(models.Model):
    user = models.ForeignKey(Coustomer, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk': self.pk})
        
class Comment(models.Model):
    user = models.ForeignKey(Coustomer, related_name = 'comments', on_delete = models.CASCADE)
    post = models.ForeignKey(Post, related_name = 'comments', on_delete = models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.body


