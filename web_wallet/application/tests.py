from decimal import Decimal
from django.db.models import Sum
from django.test import TestCase
from rest_framework import status
from application.models import Wallet, Transaction


class TestE2eWallets(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            Wallet.objects.create(label=f'cutie {i}')

    def test_wallet_list(self):
        response = self.client.get(
            '/api/v1/wallets/',
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['meta']['pagination']['count'], 5)

    def test_wallet_create(self):
        label = 'cutie 7'
        request_body = {"label": label}
        response = self.client.post(
            '/api/v1/wallets/', 
            data=request_body
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Wallet.objects.get(label__exact=label))


class TestE2eTransactions(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            Wallet.objects.create(label=f'cutie {i}')

    def test_wallet_create_income(self):
        wallet_id = 1
        amount = "100.04"

        request_body = {
            "amount": amount,
            "wallet_id": wallet_id,
            "transaction_type": True
        }
        response = self.client.post(
            '/api/v1/transactions/', 
            data=request_body
        )
        
        wallet = Wallet.objects.get(pk=wallet_id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(wallet.balance, Decimal(amount))

    def test_wallet_create_withdrawal(self):
        wallet_id = 1
        amount = "50.04"

        request_body = {
            "amount": amount,
            "wallet_id": wallet_id,
            "transaction_type": False
        }
        response = self.client.post(
            '/api/v1/transactions/', 
            data=request_body
        )
        
        wallet = Wallet.objects.get(pk=wallet_id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(wallet.balance, Decimal("-50.04"))
