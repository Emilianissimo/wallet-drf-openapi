import uuid

from decimal import Decimal
from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=255, null=False)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wallets'


class Transaction(models.Model):
    txid = models.CharField(max_length=36, null=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=18, decimal_places=2, null=False)
    transaction_type = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'

    @staticmethod
    def create_txid():
        return str(uuid.uuid4())
