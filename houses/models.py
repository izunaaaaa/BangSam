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


class Option(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Safetyoption(CommonModel):
    name = models.CharField(max_length=255)
    description = models.TextField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class House(CommonModel):
    class RoomKindChoices(models.TextChoices):
        ONE_ROOM = ("ONE_ROOM", "원룸")
        HOME = ("HOME", "주택")
        APART = ("APART", "아파트")
        VILLA = ("VILLA", "빌라")
        OFFICETEL = ("OFFICETEL", "오피스텔")
        SHARE_HOUSE = ("SHARE_HOUSE", "쉐어하우스")

    class SellKindChoices(models.TextChoices):
        SALE = ("SALE", "매매")
        CHARTER = ("CHARTER", "전세")
        MONTHLY_RENT = ("MONTHLY_RENT", "월세")

    title = models.CharField(max_length=100)  # 방 이름

    sale = models.BigIntegerField(default=0)  # 매매가

    deposit = models.BigIntegerField(default=0)  # 보증금

    monthly_rent = models.PositiveIntegerField(default=0)  # 월세

    maintenance_cost = models.PositiveIntegerField(default=0)  # 관리비

    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="host",
    )

    room = models.PositiveIntegerField(default=0)
    toilet = models.PositiveIntegerField(default=0)
    pyeongsu = models.PositiveIntegerField(default=0)
    room_kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    sell_kind = models.CharField(
        max_length=20,
        choices=SellKindChoices.choices,
    )
    address = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    visited = models.PositiveIntegerField(
        editable=False,
        default=0,
    )
    is_sale = models.BooleanField(default=True)

    dong = models.ForeignKey(
        "houses.Dong_list",
        on_delete=models.CASCADE,
    )

    option = models.ManyToManyField("houses.Option")
    Safetyoption = models.ManyToManyField(
        "houses.Safetyoption",
        related_name="safetyoption",
    )

    @property
    def gu(self):
        return self.dong.gu.name

    @property
    def thumnail(self):
        if self.Image.all().count() > 0:
            return self.Image.all()[0].url
        else:
            return ""

    def __str__(self) -> str:
        return f"{self.pk}"

    class Meta:
        ordering = ["-created_at"]
