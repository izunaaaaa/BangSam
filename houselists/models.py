from django.db import models
from users.models import User
from common.models import CommonModel


class HouseList(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    recently_views = models.ManyToManyField(
        "houses.House",
    )

    def save(self, *args, **kwargs):
        MAX_RECENTLY_HOUSES = 10

        recently_viewed_houses = self.recently_views.all()

        if recently_viewed_houses.count() > MAX_RECENTLY_HOUSES:
            oldest_houses = recently_viewed_houses.order_by("-updated_at")
            oldest_houses_to_remove = oldest_houses[MAX_RECENTLY_HOUSES:]
            self.recently_views.remove(*oldest_houses_to_remove)

        super(HouseList, self).save(*args, **kwargs)
