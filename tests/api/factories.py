import factory


class PurchaseRegistrationRequestFactory(factory.DictFactory):
    class Meta:
        exclude = ("user_entity", "store_entity")

    user_entity = factory.SubFactory("tests.authentication.factories.CustomUserFactory")
    store_entity = factory.SubFactory("tests.stores.factories.StoreFactory")

    user = factory.LazyAttribute(lambda o: o.user_entity.tax_id)
    store = factory.LazyAttribute(lambda o: o.store_entity.id)
    item_id = factory.sequence(lambda n: str(n))
    item_qty = factory.sequence(lambda n: n)
