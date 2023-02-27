from django.db import models
from common.models import CommonModel


class Review(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    house = models.ForeignKey(
        "houses.House",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    comment = models.TextField()
