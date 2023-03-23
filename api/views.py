from rest_framework.views import APIView
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status

from .services import WhatsAppService
from .serializers import PurchaseSerializer
from .utils import select_relevant_campaign_user_list
from authentication.models import CustomUser


class RegisterPurchase(APIView):
    """_summary_
    Endpoint for registering a new purchase.
    """

    serializer_class = PurchaseSerializer

    def post(self, request, format=None):
        purchase = PurchaseSerializer(data=request.data)
        if purchase.is_valid():
            purchase.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(purchase.errors, status=status.HTTP_400_BAD_REQUEST)


class PeriodicNotificationView(APIView):
    """
    Endpoint for sending a periodic notification to users.
    """

    def post(self, request=None, format=None):
        users = CustomUser.objects.all()
        whatsapp_service = WhatsAppService()
        for user in users:
            campaign_user_list = select_relevant_campaign_user_list(user)
            if len(campaign_user_list) > 0:
                whatsapp_service.send_periodic_message(*campaign_user_list)

        return Response(status=status.HTTP_200_OK)
