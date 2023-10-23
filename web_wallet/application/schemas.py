from drf_yasg import openapi


WALLET_OPENAPI_REQUEST_BODY_SCHEMA = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "type": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default='WalletList'
                        ),
                        "attributes": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "label": openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    }
                )
            },
        )


WALLET_DETAIL_OPENAPI_REQUEST_BODY_SCHEMA = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "type": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default='WalletDetail'
                        ),
                        "attributes": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "label": openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    }
                )
            },
        )

TRANSACTION_OPENAPI_REQUEST_BODY_SCHEMA = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "type": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default='TransactionList'
                        ),
                        "attributes": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "wallet_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "transaction_type": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "amount": openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            },
        )
