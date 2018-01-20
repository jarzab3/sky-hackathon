import datetime
from django.db import models
from django.contrib.auth.models import User

# from regression.choices import *


class User(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    # Extra fields
    description = models.CharField(max_length=800, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    last_edited = models.TimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Problems(models.Model):
    title = models.CharField(max_length=200)
    problemDescription = models.CharField(max_length=200)
    keywords = models.CharField(default="none", max_length=200)
    status = models.CharField(default="no resolved", max_length=200)
    frequency = models.IntegerField(default=1)
    last_query_time = models.TimeField(default=datetime.datetime.utcnow)

    # Extra fields
    description = models.CharField(max_length=800, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)