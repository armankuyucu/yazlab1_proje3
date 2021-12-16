from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Document(models.Model):
    title = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # the relationship between user and document tables
    pdf = models.FileField(upload_to='media/pdfs')

    def __str__(self):
        return self.title
