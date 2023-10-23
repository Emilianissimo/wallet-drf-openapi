import logging
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from application.models import Transaction
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from application.renderers import JSONOpenAPIRenderer
from application.schemas import (
    TRANSACTION_OPENAPI_REQUEST_BODY_SCHEMA
    )
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from application.v1.transactions.serializers import TransactionSerializer, CreateTransactionSerializer, FilterTransactionSerializer


logger = logging.getLogger(__name__)


class TransactionList(APIView, JsonApiPageNumberPagination):
    @swagger_auto_schema(
        tags=['transactions'],
        operation_summary='Transaction list',
        responses={
            status.HTTP_200_OK: TransactionSerializer()
        },
        renderer_classes=[JSONOpenAPIRenderer],
        query_serializer=FilterTransactionSerializer()
    )
    def get(self, request):
        logger.info("Opening v1 wallet list")

        txid = request.GET.get('txid', '')
        order_by = request.GET.get('created_at', '-created_at')
        wallet_id = request.GET.get('wallet_id')

        transactions = Transaction.objects\
            .filter(wallet_id=wallet_id)\
            .filter(txid__icontains=txid).order_by(order_by)
        transactions = self.paginate_queryset(transactions, request, view=self)
        serializer = TransactionSerializer(transactions, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
    

    @swagger_auto_schema(
        tags=['transactions'],
        operation_summary='Create Transaction',
        as_form_body=True,
        responses={
            status.HTTP_201_CREATED: TransactionSerializer(),
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid data',
        },
        renderer_classes=[JSONOpenAPIRenderer],
        request_body=TRANSACTION_OPENAPI_REQUEST_BODY_SCHEMA
    )
    def post(self, request):
        logger.info(f"Creating new transaction")
        serializer = CreateTransactionSerializer(data=request.data, context={'request': request})
        logger.debug({
            'msg': 'Checking data to be valid',
            'request': request.data
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning({
            'msg': 'Data is invalid',
            'request': request.data
        })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TransactionDetail(APIView):
    def get_object(self, pk):
        logger.debug(f"Trying to get transaction, id = {pk}")
        try:
            return Transaction.objects.get(id=pk)
        except Transaction.DoesNotExist:
            logger.warning(f"Transaction Id {pk} is not found")
            raise Http404

    @swagger_auto_schema(
        tags=['transactions'],
        operation_summary='Delete transaction',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid data',
        },
        renderer_classes=[JSONOpenAPIRenderer]
    ) 
    def delete(self, request, pk):
        logger.info(f"Deleting transaction for id {pk}")
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
