from django.db import models
from common.models import CommonModel


class House(CommonModel):
    class RoomKindChoices(models.TextChoices):
        ONE_ROOM = ("one_room", "One Room")
        TWO_ROOM = ("two_room", "Two Room")

    class CellKindChoices(models.TextChoices):
        MONTHLY_RENT = ("monthly_rent", "Monthly Rent")  # 월세
        SALE = ("sale", "Sale")  # 매매

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="owner",
    )
    realtor = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="realtor",
    )
    room_kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    cell_kind = models.CharField(
        max_length=20,
        choices=CellKindChoices.choices,
    )
    address = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    visited = models.PositiveIntegerField()
