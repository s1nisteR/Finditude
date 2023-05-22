from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=1024)
    myReports = models.JSONField(default=list)
    myFindings = models.JSONField(default=list)

    username = None

    #Login with email at all times
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class MissingPerson(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=255)
    identifying_info = models.CharField(max_length=100000)
    contact = models.CharField(max_length=255)


class MissingImage(models.Model):
    uuid = models.BigAutoField(primary_key=True)
    missingid = models.BigIntegerField()
    photo = models.ImageField(upload_to='missingImages/')

class MissingPersonLocations(models.Model):
    uuid = models.BigAutoField(primary_key=True)
    missingid = models.BigIntegerField()
    lattitude = models.CharField(max_length=2056)
    longitude = models.CharField(max_length=2056)

