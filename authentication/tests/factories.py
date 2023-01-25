import factory

from authentication.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    class Params:
        superuser = factory.Trait(is_superuser=True, is_staff=True)

    tax_id = factory.Faker("cpf", locale="pt_BR")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
