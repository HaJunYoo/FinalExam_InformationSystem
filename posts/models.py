from django.db import models
from accounts.models import Profile

class Books(models.Model):
    title = models.TextField()
    subtitle = models.TextField()
    isbn13 = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    url = models.TextField()
    genre = models.CharField(max_length=80, default='Algorithm')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title