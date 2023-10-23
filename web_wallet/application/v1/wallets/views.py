import logging
from django.http import Http404
from rest_framework import status
from application.models import Wallet
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from application.renderers import JSONOpenAPIRenderer
from application.schemas import (
    WALLET_OPENAPI_REQUEST_BODY_SCHEMA,
    WALLET_DETAIL_OPENAPI_REQUEST_BODY_SCHEMA
    )
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from application.v1.wallets.serializers import WalletSerializer, CreateWalletSerializer, UpdateWalletSerializer, FilterWalletSerializer


logger = logging.getLogger(__name__)


class WalletList(APIView, JsonApiPageNumberPagination):
    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Wallet list',
        responses={
            status.HTTP_200_OK: WalletSerializer()
        },
        renderer_classes=[JSONOpenAPIRenderer],
        query_serializer= FilterWalletSerializer
    )
    def get(self, request):
        logger.info("Opening v1 wallet list")

        label = request.GET.get('label', '')
        order_by = request.GET.get('created_at', '-created_at')

        wallets = Wallet.objects.filter(label__icontains=label).order_by(order_by)
        wallets = self.paginate_queryset(wallets, request, view=self)
        serializer = WalletSerializer(wallets, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
    

    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Create wallet',
        as_form_body=True,
        responses={
            status.HTTP_201_CREATED: WalletSerializer(),
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid data',
        },
        renderer_classes=[JSONOpenAPIRenderer],
        request_body=WALLET_OPENAPI_REQUEST_BODY_SCHEMA
    )
    def post(self, request):
        logger.info(f"Creating new wallet")
        serializer = CreateWalletSerializer(data=request.data, context={'request': request})
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


class WalletDetail(APIView):
    def get_object(self, pk):
        logger.debug(f"Trying to get wallet, id = {pk}")
        try:
            return Wallet.objects.get(id=pk)
        except Wallet.DoesNotExist:
            logger.warning(f"Wallet Id {pk} is not found")
            raise Http404


    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Update wallet',
        request_body=WALLET_DETAIL_OPENAPI_REQUEST_BODY_SCHEMA,
        as_form_body=True,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid data',
        },
        renderer_classes=[JSONOpenAPIRenderer]
    )
    def put(self, request, pk):
        logger.info(f"Updating  wallet for id {pk}")
        wallet = self.get_object(pk=pk)
        serializer = UpdateWalletSerializer(wallet, data=request.data, context={'request': request})

        logger.debug({
            'msg': 'Checking data to be valid',
            'request': request.data
        })
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        logger.warning({
            'msg': 'Data is invalid for wallet updating',
            'request': request.data
        })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @swagger_auto_schema(
        tags=['wallet'],
        operation_summary='Delete wallet',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid data',
        },
        renderer_classes=[JSONOpenAPIRenderer]
    ) 
    def delete(self, request, pk):
        logger.info(f"Deleting wallet for id {pk}")
        # try:
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
