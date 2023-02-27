from django.db import models
from common.models import CommonModel


class Review(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    house = models.ForeignKey("houses.House", on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
