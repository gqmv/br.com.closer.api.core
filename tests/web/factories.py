import factory


class UserRegistrationFormDataFactory(factory.DictFactory):
    tax_id = factory.Faker("ssn", locale="pt_BR")
    phone_number = factory.sequence(lambda n: f"+55819{n:08d}")
    first_name = factory.Faker("first_name")

    accept_terms = True