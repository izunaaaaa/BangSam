from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers
from .models import House


class Houses(APIView):
    def get(self, request):
        room_params = request.query_params.get("room_kind")
        cell_params = request.query_params.get("cell_kind")

        # filter_keyword : room/cell
        if room_params != None or cell_params != None:
            if room_params != None and cell_params != None:
                house = House.objects.filter(
                    room_kind=room_params, cell_kind=cell_params
                )
            elif room_params != None and cell_params == None:
                house = House.objects.filter(room_kind=room_params)

            elif room_params == None and cell_params != None:
                house = House.objects.filter(cell_kind=cell_params)

        else:
            house = House.objects.all()

        # sort_by : price/visited
        sort_by = request.GET.get("sort_by")

        if sort_by == "row_price":
            house = House.objects.order_by("price")
        elif sort_by == "visited":
            house = House.objects.order_by("-visited")
        elif sort_by == "latest":
            house = House.objects.order_by("-created_at")
        # 평점순

        # sort_count : room/toilet/pyeong
        sort_count = request.GET.get("sort_count")

        if sort_count != None:
            if sort_count == "room_1":
                house = House.objects.filter(room=1)
            elif sort_count == "room_2":
                house = House.objects.filter(room=2)
            elif sort_count == "room_3":
                house = House.objects.filter(room=3)
            elif sort_count == "room_4":
                house = House.objects.filter(room__gte=4)

            if sort_count == "toilet_1":
                house = House.objects.filter(toilet=1)
            elif sort_count == "toilet_2":
                house = House.objects.filter(toilet=2)
            elif sort_count == "toilet_3":
                house = House.objects.filter(toilet=3)
            elif sort_count == "toilet_4":
                house = House.objects.filter(toilet__gte=4)

            if sort_count == "pyeongsu_10":
                house = House.objects.filter(pyeongsu__range=(10, 19))
            elif sort_count == "pyeongsu_20":
                house = House.objects.filter(pyeongsu__range=(20, 29))
            elif sort_count == "pyeongsu_30":
                house = House.objects.filter(pyeongsu__range=(30, 39))
            elif sort_count == "pyeongsu_40":
                house = House.objects.filter(pyeongsu__gt=40)

        # filter_range : price
        start_price = request.GET.get("start_price")
        end_price = request.GET.get("end_price")

        if start_price != None and end_price != None:
            house = House.objects.filter(price__range=(start_price, end_price))

        serializer = serializers.HouseSerializer(
            house,
            many=True,
        )

        return Response(serializer.data)


class HouseDetail(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        house = self.get_object(pk)
        house.visited += 1
        house.save()
        serializer = serializers.HouseDetailSerializer(house)
        return Response(serializer.data)


from .models import Dong_list


class Delete(APIView):
    def get(self, request):
        Dong_list.objects.all().delete()
        return Response({"delete": "success"})
