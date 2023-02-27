from django.db import models
from common.models import CommonModel


class Wishlist(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    house = models.ManyToManyField(
        "houses.House",
        related_name="wishlist",
    )
