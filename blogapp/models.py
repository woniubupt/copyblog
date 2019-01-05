# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

class Blog(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=200)
    pic = models.ImageField(upload_to='mypics/')
    authorId = models.IntegerField()
    isDelete = models.BooleanField(default=1)
