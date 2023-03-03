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
        MONTHLY_RENT = ("월세", "월세")
        CHARTER = ("전세", "전세")
        SALE = ("매매", "매매")
        WHATEVER = ("상관없음", "상관없음")

    # address_gu
    # address_dong 클래스로 따로 빼기
    title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    price = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

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
    room = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    toilet = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    pyeongsu = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    distance_to_station = models.PositiveIntegerField(
        null=True,
        blank=True,
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

    photo = models.URLField(
        null=True,
        blank=True,
    )
    station_distance = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    description = models.TextField()
    visited = models.PositiveIntegerField(
        editable=False,
        default=0,
    )

    def __str__(self) -> str:
        return f"{self.owner}'s Room"


class Keyword(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(
        max_length=150,
        null=True,
        blank=True,
    )
