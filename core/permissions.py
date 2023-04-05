from rest_framework import permissions
from rest_framework.request import Request
from django.views.generic.base import View
from django.conf import settings
import logging

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


class GCPServicePermission(permissions.BasePermission):
    """
    This permission is used to ensure that only GCP services can access the endpoints protected by it.
    It uses the google-auth library to verify the JWT Token.

    * WARNING: THIS IS EXTREMELY SECURITY CRITICAL AND SHOULD NOT BE CHANGED WITHOUT THOROUGH CONSIDERATION AND TESTING *
    """

    def validate_claims(self, claims: dict, service_account: str | None):
        """
        This method is used to validate the claims of the token.
        """
        # When no service accounts are defined, the permission is never granted.
        if not service_account:
            return False

        if claims["azp"] == service_account:
            return True

        return False

    def _has_permission(self, request: Request, view: View):
        """
        This method is called by the DRF to check if the request has permission to access the endpoint.
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return False

        # split the auth type and value from the header.
        auth_type, token = auth_header.split(" ", 1)

        if auth_type.lower() != "bearer":
            return False

        try:
            claims = id_token.verify_oauth2_token(
                token, request=google_requests.Request()
            )
        except ValueError:
            return False

        return self.validate_claims(claims, settings.GOOGLE_FUNCTION_SERVICE_ACCOUNT)

    def has_permission(self, request: Request, view: View):
        """
        This method is called by the DRF to check if the request has permission to access the endpoint.
        """
        logging.getLogger(__name__).info("GCP Authenticated request received.")
        result = self._has_permission(request, view)

        if not result:
            logging.getLogger(__name__).error(
                "GCP Authenticated request failed to authenticate. This might be a security issue."
            )

        return result
