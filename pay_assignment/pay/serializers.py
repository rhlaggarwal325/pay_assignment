from rest_framework import serializers
from .models import Transaction, Wallet

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['text', 'amount']