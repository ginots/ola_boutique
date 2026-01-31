from django.db import models

# Create your models here.

class TableCustomer(models.Model):
    name=models.CharField(max_length=100, null=True)
    phone=models.IntegerField(null=True)
    email=models.EmailField(max_length=50,null=True)
    address=models.TextField(null=True)


