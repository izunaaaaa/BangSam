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

    # def save(self, *args, **kwargs):
    #     MAX_RECENTLY_HOUSES = 10

    #     viewed_houses = self.recently_views.all()

    #     if viewed_houses.count() > MAX_RECENTLY_HOUSES:
    #         oldest_houses = viewed_houses.order_by("created_at")
    #         oldest_houses_to_remove = oldest_houses[MAX_RECENTLY_HOUSES:]
    #         self.recently_views.remove(*oldest_houses_to_remove)

    #     super(HouseList, self).save(*args, **kwargs)

    # if viewed_houses.count() >= MAX_RECENTLY_HOUSES:
    #     oldest_houses = viewed_houses[MAX_RECENTLY_HOUSES:]
    #     self.recently_views.remove(*oldest_houses)

    # super(HouseList, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        MAX_RECENTLY_HOUSES = 10

        viewed_houses = self.recently_views.order_by("created_at")

        if viewed_houses.count() > MAX_RECENTLY_HOUSES:
            oldest_houses = viewed_houses[:MAX_RECENTLY_HOUSES]
            houses_to_remove = viewed_houses[MAX_RECENTLY_HOUSES:]
            self.recently_views.remove(*houses_to_remove)

    super(HouseList, self).save(*args, **kwargs)
