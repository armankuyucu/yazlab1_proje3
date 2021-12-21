from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Document(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # the relationship between user and document tables
    author = models.CharField(max_length=200)
    pdf = models.FileField()
    student_id = models.CharField(max_length=20)
    type_of_education = models.CharField(max_length=200)
    lecture_name = models.CharField(max_length=200)
    abstract = models.TextField()
    term = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    advisor = models.CharField(max_length=200)
    jury = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# class PDFInfo(models.Model):
#     name = models.CharField(max_length=200)
#     student_id = models.CharField(max_length=20)
#     type_of_education = models.CharField(max_length=200)
#     lecture_name = models.CharField(max_length=200)
#     abstract = models.TextField()
#     term = models.CharField(max_length=200)
#     title = models.CharField(max_length=200)
#     keywords = models.CharField(max_length=200)
#     advisor = models.CharField(max_length=200)
#     jury = models.CharField(max_length=200)
