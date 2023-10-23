from django.urls import path
from application.v1.views import HealthCheckView
from application.v1.wallets.views import WalletList, WalletDetail
from application.v1.transactions.views import TransactionList, TransactionDetail

urlpatterns = [
    path('', HealthCheckView.as_view(), name='application.v1.health-check'),

    path('wallets/', WalletList.as_view(), name='application.v1.wallets'),
    path('wallets/<int:pk>/', WalletDetail.as_view(), name='application.v1.wallets.detail'),

    path('transactions/', TransactionList.as_view(), name='application.v1.wallets'),
    path('transactions/<int:pk>/', TransactionDetail.as_view(), name='application.v1.wallets.detail'),
]
