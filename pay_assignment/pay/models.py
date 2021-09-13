from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Wallet(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    money_added = models.IntegerField(default=0)
    money_paid = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.text