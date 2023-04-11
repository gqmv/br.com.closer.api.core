import pytest

from stores.services import (
    AbstractPOSService,
    AbstractPOSServiceRegistry,
    DummyPOSService,
    get_pos_service,
)


class TestAbstractPOSServiceRegistry:
    def test_get_dummy_service(self):
        service = AbstractPOSServiceRegistry.get_service("dummy")
        assert service == DummyPOSService

    def test_get_django_choices(self):
        choices = AbstractPOSServiceRegistry.get_django_choices()
        assert choices == [("dummy", "dummy")]

    def test_register_service(self):
        class TestService(AbstractPOSService):
            _pos_service_name = "test"

        assert AbstractPOSServiceRegistry.get_service("test") == TestService
        assert AbstractPOSServiceRegistry.get_django_choices() == [
            ("dummy", "dummy"),
            ("test", "test"),
        ]


class TestGetPOSService:
    def test_get_dummy_service(self):
        service = get_pos_service("dummy")
        assert service == DummyPOSService


class TestDummyPOSService:
    def test_generate_coupon_code(self):
        service = DummyPOSService()
        coupon_code = service.generate_coupon_code(None, None, None)
        assert coupon_code == "XXX-YYY-ZZZ"
