from abc import ABC, abstractmethod, ABCMeta


class AbstractPOSServiceRegistry(ABCMeta):
    """
    Abstract metaclass for POS service registries.
    """

    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_class = type.__new__(cls, name, bases, attrs)
        if hasattr(new_class, "_pos_service_name"):
            cls.REGISTRY[new_class._pos_service_name] = new_class

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def get_service(cls, service_name: str) -> "AbstractPOSService":
        """
        Returns the service with the given name.
        """
        return cls.REGISTRY[service_name]

    @classmethod
    def get_django_choices(cls) -> list[tuple[str, str]]:
        """
        Returns a list of tuples that can be used as choices in a Django model.
        """
        choices = []
        for service_name, _ in cls.REGISTRY.items():
            choices.append((service_name, service_name))
        return choices


class AbstractPOSService(ABC, metaclass=AbstractPOSServiceRegistry):
    """
    Abstract class for POS services.
    """

    @abstractmethod
    def generate_coupon_code(
        self, store: "stores.models.Store", reward_id: str, reward_qty: int
    ) -> str:
        """
        Generates a coupon code for a given store, reward id and reward quantity.
        """
        ...


def get_pos_service(service_name: str) -> AbstractPOSService:
    """
    Returns the POS service with the given name.
    """
    return AbstractPOSServiceRegistry.get_service(service_name)


class DummyPOSService(AbstractPOSService):
    """
    Dummy POS service that should be used for testing purposes.
    """

    _pos_service_name = "dummy"

    def generate_coupon_code(
        self, store: "stores.models.Store", reward_id: str, reward_qty: int
    ) -> str:
        return "XXX-YYY-ZZZ"
