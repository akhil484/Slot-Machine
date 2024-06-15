from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account_Information(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_month_balance = models.IntegerField(default=5000)
    no_of_wins = models.IntegerField(default=0)
