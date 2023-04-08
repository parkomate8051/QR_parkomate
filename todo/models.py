from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class registered_info(models.Model):
    name = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    BG = models.CharField(max_length=10)
    M_F = models.CharField(max_length=10)
    BMI = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
