from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField()
    intro=models.TextField()
    body=models.TextField()
    image=models.ImageField(upload_to='media',blank=True)
    date_added=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering=['-date_added']

class Comment(models.Model):
    post=models.ForeignKey(Blog,related_name='comment',on_delete=models.CASCADE)
    email=models.EmailField()
    body=models.TextField()
    name=models.CharField(max_length=100,default='inconnu')
    date_added=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-date_added']
class Like(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    date_creation = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-date_creation']