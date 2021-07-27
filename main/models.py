from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    address = models.TextField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
