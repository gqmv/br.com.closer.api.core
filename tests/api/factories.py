import factory


class PurchaseRegistrationRequestFactory(factory.DictFactory):
    class Meta:
        exclude = ("user", "store")

    user = factory.SubFactory("tests.authentication.factories.CustomUserFactory")
    store = factory.SubFactory("tests.stores.factories.StoreFactory")

    user_tax_id = factory.LazyAttribute(lambda o: o.user.tax_id)
    store_id = factory.LazyAttribute(lambda o: o.store.id)
    item_id = factory.sequence(lambda n: str(n))
    item_qty = factory.sequence(lambda n: n)
