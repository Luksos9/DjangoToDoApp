from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)  # auto adds time with creation
    completed = models.DateTimeField(null=True)  # null -
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class User(models.Model):
    pass
