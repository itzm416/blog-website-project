from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to="profile_image/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    
class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    views = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='thumbnail/')
    add_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.content
    

class SubComment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    reply = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)
    content = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.content
