from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  
  def __str__(self):
    return f"{self.firstname} {self.lastname}"


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    report = models.FileField(upload_to='pdf', null=True)
    
    def __str__(self):
        return f"{self.author}"
    
    
class Review(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()