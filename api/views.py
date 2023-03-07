from rest_framework.views import APIView
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .serializers import PurchaseSerializer
from .utils import select_relevant_campaigns
from authentication.models import CustomUser
from stores.models import CampaignUser, RegularCampaign, Store


class RegisterPurchase(APIView):
    """_summary_
    Endpoint for registering a new purchase.
    """

    serializer_class = PurchaseSerializer

    def post(self, request, format=None):
        purchase = PurchaseSerializer(data=request.data)
        if not purchase.is_valid():
            return Response(purchase.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = purchase.validated_data

        errors = {}
        try:
            user = CustomUser.objects.get(tax_id=validated_data.get("user_tax_id"))
        except CustomUser.DoesNotExist:
            errors["user_tax_id"] = ["User with this tax id does not exist."]

        try:
            store = Store.objects.get(id=validated_data.get("store_id"))
        except Store.DoesNotExist:
            errors["store_id"] = ["Store with this id does not exist."]

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        campaigns = RegularCampaign.objects.filter(
            store=store, item_id=validated_data.get("item_id")
        )
        for campaign in campaigns:
            try:
                campaign_user = CampaignUser.objects.get(campaign=campaign, user=user)
            except CampaignUser.DoesNotExist:
                campaign_user = CampaignUser.objects.create(
                    campaign=campaign, user=user
                )

            campaign_user.progress = F("progress") + validated_data.get("item_qty")
            campaign_user.save()

            campaign_user.refresh_from_db()
            while campaign_user.progress >= campaign.item_qty:
                coupon = generate_coupon(
                    campaign.store, campaign.reward_id, campaign.reward_qty
                )
                notify_coupon(user, coupon, campaign_user)
                campaign_user.progress = F("progress") - campaign.item_qty
                campaign_user.save()
                campaign_user.refresh_from_db()

        return Response(status=status.HTTP_200_OK)


class PeriodicNotificationView(APIView):
    """
    Endpoint for sending a periodic notification to users.
    """

    def post(self, request, format=None):
        users = CustomUser.objects.all()
        for user in users:
            campaigns = select_relevant_campaigns(user)
            periodic_notification(user, *campaigns)

        return Response(status=status.HTTP_200_OK)
