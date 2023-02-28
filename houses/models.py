from django.db import models
from common.models import CommonModel


class House(CommonModel):
    class RoomKindChoices(models.TextChoices):
        ONE_ROOM = ("원룸", "원룸")
        TWO_ROOM = ("투룸", "투룸")
        THREE_ROOM = ("쓰리룸", "쓰리룸")
        OFFICETEL = ("오피스텔", "오피스텔")
        APART = ("아파트", "아파트")

    class CellKindChoices(models.TextChoices):
        MONTHLY_RENT = ("월세", "월세")  # 월세
        SALE = ("매매", "매매")  # 매매

    # title char
    # address_gu
    # address_dong 클래스로 따로 빼기
    # keyword char

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
    address = models.CharField(max_length=100)
    description = models.TextField()
    visited = models.PositiveIntegerField(editable=False, default=0)

    def __str__(self) -> str:
        return f"{self.owner}'s Room"
