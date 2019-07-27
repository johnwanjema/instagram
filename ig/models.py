from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    profile_photo = models.ImageField(upload_to='profilepics')
    bio = models.CharField(max_length=2000)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        ordering = ('user',)


    def __str__(self):
        return self.profile_photo

class Image(models.Model):
    photo = models.ImageField(upload_to='photos')
    image_name = models.CharField(max_length=100)
    image_caption = models.CharField(max_length=2000)
    post_date = models.DateTimeField(auto_now=True)
    likes = models.BooleanField(default=False)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('post_date',)

    def __str__(self):
        return self.photo

class Comment(models.Model):
    comment = models.CharField(max_length=50)
    posted_on = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('posted_on',)

    def __str__(self):
        return self.comment
