from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return f'{self.name}'


class Advertisement(models.Model):
    name = models.CharField(max_length=120, unique=True)
    content = FroalaField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Reaction(models.Model):
    new = 'N'
    accept = 'A'
    refused = 'R'

    STATUS_TYPES = [
        (new, 'Новый'),
        (accept, 'Принят'),
        (refused, 'Отклонен')
    ]

    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_TYPES, default=new)


class News(models.Model):
    name = models.CharField(max_length=120, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    content = FroalaField()


