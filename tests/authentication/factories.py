import factory

from authentication.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    class Params:
        superuser = factory.Trait(is_superuser=True, is_staff=True)
        generate_password = factory.Trait(password=factory.Faker("password"))

    tax_id = factory.Faker("cpf", locale="pt_BR")
    phone_number = factory.sequence(lambda n: f"+55819{n:08d}")
    first_name = factory.Faker("first_name")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
