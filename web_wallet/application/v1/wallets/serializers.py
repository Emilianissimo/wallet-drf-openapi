from decimal import Decimal
from application.models import Wallet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FilterWalletSerializer(serializers.Serializer):
    label = serializers.CharField(required=False)
    order_by = serializers.CharField(required=False)


class WalletSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    label = serializers.CharField(required=False, max_length=255)
    balance = serializers.DecimalField(max_digits=18, decimal_places=2, min_value=Decimal(0), required=True)

    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance']


class CreateWalletSerializer(serializers.Serializer):
    label = serializers.CharField(required=True)

    def create(self, validated_data):
        return Wallet.objects.create(label=validated_data.get('label'))
    

class UpdateWalletSerializer(serializers.Serializer):
    label = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label')
        instance.save()
        return instance
