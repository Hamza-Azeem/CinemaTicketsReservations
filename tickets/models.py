from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=20)
    date = models.DateField()

class Guest(models.Model):
    name = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)

class Reservation(models.Model):
    movie = models.ForeignKey(Movie, on_delete= models.CASCADE, related_name='reservation')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservation')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)