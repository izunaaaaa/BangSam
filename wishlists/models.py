from django.db import models
from common.models import CommonModel


class Wishlist(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    house = models.ManyToManyField(
        "houses.House",
        related_name="wishlist",
    )

    def __str__(self) -> str:
        return f"{self.user}'s wishlist"
