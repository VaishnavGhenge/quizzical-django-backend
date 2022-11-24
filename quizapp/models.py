from django.db import models

class UserData(models.Model):
    _id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    highestscore = models.BigIntegerField(default=0)