from django.db import models
from django.contrib.auth.models import User
from django import forms

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  
  def __str__(self):
    return f"{self.firstname} {self.lastname}"


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdf', null=True)
    
    def __str__(self):
        return f"report ID{self.id} {self.author} - {self.title}"
    
    
class Review(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()