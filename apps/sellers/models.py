from apps.common.models import PersonBase

class Seller(PersonBase):

    class Meta:
        db_table = "sellers"