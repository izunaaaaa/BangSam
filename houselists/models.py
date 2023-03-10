from django.db import models
from users.models import User
from common.models import CommonModel

# from django.utils import timezone


class Houselist(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    house = models.ManyToManyField(
        "houses.House",
    )
    # viewed_at = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     ordering = ["-created_at"]
    # 최근 조회순으로 정렬

    def save(self, *args, **kwargs):
        # 현재 사용자가 최근에 본 집 목록에서 house 정보를 최대 10개까지만 유지
        MAX_RECENTLY_VIEWED_HOUSES = 10
        user_recently_viewed_houses = Houselist.objects.filter(user=self.user)
        # user_recently_viewed_houses = self.house.all()
        if user_recently_viewed_houses.count() >= MAX_RECENTLY_VIEWED_HOUSES:
            oldest_house = user_recently_viewed_houses.order_by("viewed_at")[0]
            oldest_house.delete()
        super().save(*args, **kwargs)  # 부모 클래스의 save() 메서드 호출

    # def add_to_recently_viewed(request, house):
    #     user = request.user
    #     # 최근 본 집 정보 추가하기
    #     RecentlyViewed.objects.create(user=user, house=house, viewed_at=timezone.now())
    #     # 최근 본 집 정보가 10개 이상인 경우, 가장 오래된 집 삭제하기
    #     viewed_houses = RecentlyViewed.objects.filter(user=user)[:10]
    #     RecentlyViewed.objects.exclude(pk__in=viewed_houses).delete()
