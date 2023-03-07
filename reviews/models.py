from django.db import models
from common.models import CommonModel
from django.core.validators import MinValueValidator, MaxValueValidator


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
    house_rating = models.PositiveIntegerField(
        default=0,
        help_text="0~5사이 값으로 입력하세요",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        null=True,
    )
    user_rating = models.PositiveIntegerField(
        default=0,
        help_text="0~5사이 값으로 입력하세요",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user} / {self.house_rating}"

    def __str__(self):
        return f"{self.user} / {self.user_rating}"
