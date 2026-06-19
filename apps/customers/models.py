from apps.common.models import PersonBase

class Customer(PersonBase):

    class Meta:
        db_table = "customers"