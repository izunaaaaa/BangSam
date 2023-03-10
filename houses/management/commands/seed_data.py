from django.core.management.base import BaseCommand
from faker import Faker
from houses.models import Dong_list
import random
from users.models import User
from houses.models import House, Dong_list, Gu_list
from images.models import Image

import json


class Command(BaseCommand):
    help = "이 커맨드를 통해 랜덤한 테스트 유저 데이터를 만듭니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            default=1,
            type=int,
            help="몇 명의 유저를 만드나",
        )

    def handle(self, *args, **options):
        if not Gu_list.objects.all():
            with open("gu_list.json", "r", encoding="UTF-8") as gu_data:
                gu = json.load(gu_data)
            for i in gu:
                Gu_list.objects.create(
                    pk=i.get("pk"),
                    name=i.get("fields").get("name"),
                )
            self.stdout.write(self.style.SUCCESS("구 리스트가 작성되었습니다."))

        if not Dong_list.objects.all():
            with open("dong_list.json", "r", encoding="UTF-8") as dong_data:
                dong_list = json.load(dong_data)
            for dong in dong_list:
                Dong_list.objects.create(
                    pk=dong.get("pk"),
                    gu=Gu_list.objects.get(pk=dong.get("fields").get("gu")),
                    name=dong.get("fields").get("name"),
                )
            self.stdout.write(self.style.SUCCESS("동 리스트가 작성되었습니다."))

        total = options.get("total")
        fake = Faker(["ko_KR"])
        new_list = []
        image_key = [
            "85b5fb3d-c23a-4e91-96cd-92c23cfec900",
            "a6e6873b-a65f-483e-27d6-18bdce658200",
            "66036eed-79fe-40fd-7adc-9a10686bbf00",
            "8dd960f2-32e3-4854-0c92-6a3b9dfb2800",
            "2512511d-6de1-4d14-97dd-517fdf5baf00",
            "942fcc68-a692-4564-aa14-55998fadb200",
        ]
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
                create_house = House.objects.create(
                    pk=House.objects.count() + 1,
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
                    is_sale=True,
                )
                for i in range(5):
                    Image.objects.create(
                        house=create_house,
                        url=f"https://imagedelivery.net/TfkiqSGnbio9VWWQtYee6A/{random.choice(image_key)}/public",
                    )
                data["owner"] = data["owner"].pk
                house["fields"] = data
                new_list.append(house)

        self.stdout.write(self.style.SUCCESS(f"{total}명의 유저가 작성되었습니다."))
