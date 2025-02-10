from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from decouple import config
import midtransclient
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser


# Create Snap API instance
snap = midtransclient.Snap(
    # Set to true if you want Production Environment (accept real transaction).
    is_production=False,
    server_key=config('SERVER_KEY_MIDTRANS')
)

class PaymentCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if "order_id" not in request.data:
            return Response({"error": "No order id sended as request"}, status=400)

        order_id = request.data.get("order_id")
        gross_amount = request.data.get("gross_amount")
        # Build API parameter
        param = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": gross_amount
            }, "credit_card":{
                "secure" : True
            }, "customer_details":{
                "first_name": "budi",
                "last_name": "pratama",
                "email": "budi.pra@example.com",
                "phone": "08111222333"
            }
        }

        transaction = snap.create_transaction(param)

        transaction_token = transaction['token']
        return Response({"status": "success", "message": "Snap successfully created", "token": transaction_token}, status=201)
