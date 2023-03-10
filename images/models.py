from django.db import models
from common.models import CommonModel


class Image(CommonModel):
    house = models.ForeignKey(
        "houses.House", on_delete=models.CASCADE, related_name="Image"
    )
    url = models.URLField()

    def __str__(self) -> str:
        return self.house.title + " 사진"
