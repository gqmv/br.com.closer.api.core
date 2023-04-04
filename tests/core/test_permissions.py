import pytest
from django.test import RequestFactory
from django.conf import settings

from core.permissions import GCPServicePermission


class TestGCPServicePermission:
    def test_has_permission_success(self, mocker):
        request = RequestFactory().get("/")

        request.headers = {"Authorization": "Bearer test-token"}

        mock_verify_oauth2_token = mocker.patch(
            "google.oauth2.id_token.verify_oauth2_token"
        )
        mock_verify_oauth2_token.return_value = {"azp": "test-service-account"}

        mock_validate_claims = mocker.patch(
            "core.permissions.GCPServicePermission.validate_claims"
        )
        mock_validate_claims.return_value = True

        response = GCPServicePermission().has_permission(request, None)

        assert response is True

        verify_oauth_args, verify_oauth_kwargs = mock_verify_oauth2_token.call_args
        assert len(verify_oauth_args) == 1
        assert len(verify_oauth_kwargs) == 1
        assert verify_oauth_args[0] == "test-token"
        assert verify_oauth_kwargs["request"] is not None

        validate_claims_args, validate_claims_kwargs = mock_validate_claims.call_args
        assert len(validate_claims_args) == 2
        assert len(validate_claims_kwargs) == 0
        assert validate_claims_args[0] == {"azp": "test-service-account"}
        assert validate_claims_args[1] == settings.GOOGLE_FUNCTION_SERVICE_ACCOUNT

    def test_has_permission_verify_oauth_error(self, mocker):
        request = RequestFactory().get("/")

        request.headers = {"Authorization": "Bearer test-token"}

        mock_verify_oauth2_token = mocker.patch(
            "google.oauth2.id_token.verify_oauth2_token"
        )
        mock_verify_oauth2_token.side_effect = ValueError()

        mock_validate_claims = mocker.patch(
            "core.permissions.GCPServicePermission.validate_claims"
        )
        mock_validate_claims.return_value = True

        response = GCPServicePermission().has_permission(request, None)

        assert response is False
        verify_oauth_args, verify_oauth_kwargs = mock_verify_oauth2_token.call_args
        assert len(verify_oauth_args) == 1
        assert len(verify_oauth_kwargs) == 1
        assert verify_oauth_args[0] == "test-token"
        assert verify_oauth_kwargs["request"] is not None

        mock_validate_claims.assert_not_called()

    def test_no_auth_header(self):
        request = RequestFactory().get("/")

        response = GCPServicePermission().has_permission(request, None)

        assert response is False

    def test_auth_type_not_bearer(self):
        request = RequestFactory().get("/")

        request.headers = {"Authorization": "Basic test-token"}

        response = GCPServicePermission().has_permission(request, None)

        assert response is False

    def test_validate_claims_success(self):
        claims = {"azp": "test-service-account"}

        response = GCPServicePermission().validate_claims(
            claims, "test-service-account"
        )

        assert response is True

    def test_validate_claims_no_service_account(self):
        claims = {"azp": "test-service-account"}

        response = GCPServicePermission().validate_claims(claims, None)

        assert response is False

    def test_validate_claims_service_account_not_equal(self):
        claims = {"azp": "test-service-account"}

        response = GCPServicePermission().validate_claims(
            claims, "test-service-account-2"
        )

        assert response is False
