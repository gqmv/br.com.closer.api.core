from abc import ABC, abstractmethod

from stores.models import Store


class AbstractPOSService(ABC):
    """
    Abstract class for POS services.
    """

    @abstractmethod
    def generate_coupon_code(
        self, store: Store, reward_id: str, reward_qty: int
    ) -> str:
        """
        Generates a coupon code for a given store, reward id and reward quantity.
        """
        ...


class DummyPOSService(AbstractPOSService):
    """
    Dummy POS service that should be used for testing purposes.
    """

    def generate_coupon_code(
        self, store: Store, reward_id: str, reward_qty: int
    ) -> str:
        return "XXX-YYY-ZZZ"
