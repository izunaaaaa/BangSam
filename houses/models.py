from django.db import models
from common.models import CommonModel
from django.core.exceptions import ValidationError


class Gu_list(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name


class Dong_list(models.Model):
    gu = models.ForeignKey(
        "houses.Gu_list",
        on_delete=models.CASCADE,
        related_name="dong",
    )
    name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.name


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

    title = models.CharField(
        max_length=100,
    )

    price = models.PositiveIntegerField(default=0)

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="owner",
        null=True,
        blank=True,
    )
    realtor = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="realtor",
        null=True,
        blank=True,
    )

    room = models.PositiveIntegerField(default=0)
    toilet = models.PositiveIntegerField(default=0)
    pyeongsu = models.PositiveIntegerField(default=0)
    distance_to_station = models.PositiveIntegerField(default=0)
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

    description = models.TextField(
        blank=True,
    )
    visited = models.PositiveIntegerField(
        editable=False,
        default=0,
    )
    is_sale = models.BooleanField(default=True)
    dong = models.ForeignKey(
        "houses.Dong_list",
        on_delete=models.CASCADE,
    )

    @property
    def gu(self):
        return self.dong.gu.name

    def __str__(self) -> str:
        return f"{self.owner}'s Room"

    def clean(self):
        if self.owner and self.realtor:
            raise ValidationError(
                "Either owner or realtor can be specified, but not both."
            )
        elif not self.owner and not self.realtor:
            raise ValidationError("Either owner or realtor must be specified.")


class Keyword(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(
        max_length=150,
        null=True,
        blank=True,
    )
