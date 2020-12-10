from django.db import models

# Create your models here.

class Result(models.Model):
    name=models.CharField(max_length=50)
    company_name=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    website=models.CharField(max_length=50)
    contact1=models.CharField(max_length=15)
    contact2=models.CharField(max_length=15)
    city=models.CharField(max_length=15)
    state=models.CharField(max_length=15)
    pincode=models.CharField(max_length=15)
    address=models.CharField(max_length=250)
    fileurl=models.CharField(max_length=100)
    filename=models.CharField(max_length=100)

