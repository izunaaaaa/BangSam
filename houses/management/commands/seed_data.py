from django.core.management.base import BaseCommand
from faker import Faker
from houses.models import Dong_list
import random
from users.models import User
from houses.models import House
import json


class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤한 테스트 유저 데이터를 만듭니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            default=2,
            type=int,
            help="몇 명의 유저를 만드나",
        )

    def handle(self, *args, **options):
        total = options.get("total")
        fake = Faker(["ko_KR"])
        new_list = []
        for i in Dong_list.objects.all():
            for k in range(total):
                house = {"model": "houses.House"}
                data = {
                    "title": fake.building_name(),
                    "price": random.randint(10, 50),
                    "owner": User.objects.get(pk=1),
                    "room": random.randint(1, 3),
                    "toilet": random.randint(1, 3),
                    "pyeongsu": random.randint(10, 50),
                    "distance_to_station": random.randint(5, 20),
                    "room_kind": random.choice(House.RoomKindChoices.values),
                    "cell_kind": random.choice(House.CellKindChoices.values),
                    "address": " ".join(i for i in fake.land_address().split(" ")[2:]),
                    "description": "인근에서 가장 좋은 방입니다.",
                }
                House.objects.create(
                    title=data["title"],
                    price=data["price"],
                    owner=data["owner"],
                    room=data["room"],
                    toilet=data["toilet"],
                    pyeongsu=data["pyeongsu"],
                    distance_to_station=data["distance_to_station"],
                    room_kind=data["room_kind"],
                    cell_kind=data["cell_kind"],
                    address=data["address"],
                    description=data["description"],
                    dong=i,
                )
                data["owner"] = data["owner"].pk
                house["fields"] = data
                new_list.append(house)
            print(i.name + "makeing")

        with open("house_data.json", "w", encoding="UTF-8") as m:
            json.dump(new_list, m, ensure_ascii=False, indent=2)
        self.stdout.write(self.style.SUCCESS(f"{total}명의 유저가 작성되었습니다."))
