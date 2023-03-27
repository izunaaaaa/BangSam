from django.db import models
from common.models import CommonModel


class HouseList(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="house_list",
    )
    recently_views = models.ForeignKey(
        "houses.House",
        on_delete=models.CASCADE,
        related_name="house_list",
    )

    def save(self, *args, **kwargs):
        while self.user.house_list.count() >= 36:
            self.user.house_list.order_by("updated_at").first().delete()

        super(HouseList, self).save(*args, **kwargs)
