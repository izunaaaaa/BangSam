from django.db import models
from common.models import CommonModel


class Image(CommonModel):
    house = models.ForeignKey("houses.House", on_delete=models.CASCADE)
    url = models.URLField()
