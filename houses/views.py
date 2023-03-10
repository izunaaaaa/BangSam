from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers
from .models import House, Gu_list, Dong_list
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Houses(APIView):
    @swagger_auto_schema(
        operation_summary="모든 방에 대한 리스트를 가져오는 api",
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="1 페이지당 24개의 데이터",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "room_kind",
                openapi.IN_QUERY,
                description="룸 타입 / 원룸, 투룸, 쓰리룸, 아파트, 오피스텔",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "cell_kind",
                openapi.IN_QUERY,
                description="사는 타입 / 월세, 전세, 매매",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "sort_by",
                openapi.IN_QUERY,
                description="정렬 타입 / 가격(row_price), 조회수(visitied), 최신순(lastest)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "sort_count",
                openapi.IN_QUERY,
                description="추가 필터 / room_1,2,3 / toilet_1,2,3 / pyeongsu_10,20,30",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "start_price",
                openapi.IN_QUERY,
                description="최소 가격 필터",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "end_price",
                openapi.IN_QUERY,
                description="최대 가격 필터",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.HouseSerializer(many=True),
            )
        },
    )
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
            house = house.order_by("price")
        elif sort_by == "visited":
            house = house.order_by("-visited")
        elif sort_by == "lastest":
            house = house.order_by("-created_at")
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

        # pagenations
        current_page = request.GET.get("page", 1)
        items_per_page = 24
        paginator = Paginator(house, items_per_page)
        try:
            page = paginator.page(current_page)
        except:
            page = paginator.page(paginator.num_pages)

        serializer = serializers.HouseSerializer(
            page,
            many=True,
        )

        data = {
            "num_pages": paginator.num_pages,
            "current_page": page.number,
            "count": paginator.count,
            "results": serializer.data,
        }
        # /?page=2파람으로 받기

        return Response(data)


class HouseDetail(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="각 방에 대한 정보를 가져오는 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.HouseDetailSerializer(),
            ),
            404: "Not Found",
        },
    )
    def get(self, request, pk):
        house = self.get_object(pk)
        house.visited += 1
        house.save()
        serializer = serializers.HouseDetailSerializer(house)
        return Response(serializer.data)


class GuList(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(
        operation_summary="구 리스트 가져오기 위한 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.GulistSerializer(many=True),
            )
        },
    )
    def get(self, request):
        gu_list = Gu_list.objects.all()
        serializer = serializers.GulistSerializer(
            gu_list,
            many=True,
        )
        return Response(serializer.data)


class DongList(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Dong_list.objects.filter(gu=pk)

        except Dong_list.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="동 리스트 가져오기 위한 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.DonglistSerializer(many=True),
            )
        },
    )
    def get(self, request, pk):
        dong_list = self.get_object(pk)
        serializer = serializers.DonglistSerializer(
            dong_list,
            many=True,
        )
        return Response(serializer.data)


class DeleteRoom(APIView):
    @swagger_auto_schema(
        operation_summary="모든 방 삭제 ( 개발용 임시 api, 사용 금지 )",
        responses={200: "OK"},
    )
    def get(self, request):
        House.objects.all().delete()
