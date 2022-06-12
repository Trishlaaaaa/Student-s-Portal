from django.db import models

# Create your models here.
class Student(models.Model):
    Name = models.CharField(max_length=50)
    EnrollNo = models.CharField(max_length=15)
    Branch=models.CharField(max_length=50)
    Section=models.CharField(max_length=50)

