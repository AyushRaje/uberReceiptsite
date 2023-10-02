from django.db import models

# Create your models here.
class Data(models.Model):
    id=models.AutoField(null=False,primary_key=True)
    Total=models.CharField(max_length=2048)
    Date=models.CharField(max_length=2048)
    Time=models.CharField(max_length=2048)
    From=models.CharField(max_length=2048)
    To=models.CharField(max_length=2048)
    Distance=models.CharField(max_length=2048)