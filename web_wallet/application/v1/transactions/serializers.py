import logging
from decimal import Decimal
from datetime import datetime
from django.http import Http404
from rest_framework import serializers
from application.models import Transaction, Wallet
from django.db import transaction as db_transaction
from web_wallet.settings import TRANSACTION_BLOCK_TTL
from rest_framework.exceptions import ValidationError
from application.v1.wallets.serializers import WalletSerializer


logger = logging.getLogger(__name__)

class FilterTransactionSerializer(serializers.Serializer):
    txid = serializers.CharField(required=False)
    wallet_id = serializers.IntegerField(required=True)
    order_by = serializers.CharField(required=False)


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    txid = serializers.CharField(required=False, max_length=255)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2, min_value=Decimal(0), required=True)
    wallet = WalletSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'txid', 'amount', 'wallet']


class CreateTransactionSerializer(serializers.Serializer):
    wallet_id = serializers.IntegerField(required=True)
    transaction_type = serializers.BooleanField(required=True)
    amount = serializers.DecimalField(required=True, min_value=Decimal(0), max_digits=18, decimal_places=2)

    def create(self, validated_data):
        with db_transaction.atomic():
            try:
                wallet = Wallet.objects.get(pk=validated_data.get('wallet_id'))
                latest_transaction = wallet.transactions.order_by('-created_at').first()
            except Wallet.DoesNotExist:
                logger.warning(f"Wallet Id {wallet.id} is not found")
                raise Http404
            
            if latest_transaction is not None:
                now = datetime.now().replace(tzinfo=None)
                latest_transaction_time = latest_transaction.created_at.replace(tzinfo=None)
                latest_transaction_diff_in_seconds = (now - latest_transaction_time).total_seconds()
            
                logger.debug(f"Checking if total seconds since the latest transaction for this wallet is ({latest_transaction_diff_in_seconds}) are bigger than {TRANSACTION_BLOCK_TTL}")
                if latest_transaction_diff_in_seconds < TRANSACTION_BLOCK_TTL:
                    raise ValidationError("Transaction couldn't be provided, please try again later") 
            
            transaction_type = validated_data.get('transaction_type')

            transaction = Transaction.objects.create(
                txid=Transaction.create_txid(),
                wallet=wallet,
                amount=validated_data.get('amount'),
                transaction_type=transaction_type
            )

            logger.debug(f"Cheking transaction type, for Withdrawal is False and for Income is True. Actual: {transaction_type}")
            if transaction_type:
                wallet.balance += transaction.amount
            else:
                wallet.balance -= transaction.amount
            wallet.save(update_fields=['balance',])
            
            return transaction
