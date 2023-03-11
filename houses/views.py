from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers
from .models import House, Gu_list, Dong_list
from houselists.models import HouseList
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q


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
                "sale_start_params",
                openapi.IN_QUERY,
                description="최소 가격 필터",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "sale_end_params",
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

        house = House.objects.all()

        # 방종류
        room_kind_params = request.query_params.get("room_kind_params")

        # 매매종류
        cell_kind_params = request.query_params.get("cell_kind_params")

        # 매매가
        sale_start_params = request.GET.get("sale_start_params")
        sale_end_params = request.GET.get("sale_end_params")

        # 보증금
        deposit_start_params = request.GET.get("deposit_start_params")
        deposit_end_params = request.GET.get("deposit_end_params")

        # 월세
        monthly_rent_start_params = request.GET.get("monthly_rent_start_params")
        monthly_rent_end_params = request.GET.get("monthly_rent_end_params")

        # 관리비
        maintenance_cost_start_params = request.GET.get("maintenance_cost_start_params")
        maintenance_cost_end_params = request.GET.get("maintenance_cost_end_params")

        # 방개수
        num_of_room = request.GET.get("num_of_room")

        # 화장실개수
        num_of_toilet = request.GET.get("num_of_toilet")

        # 평수
        pyeongsu = request.GET.get("pyeongsu")

        # 주소(서울시, 구, 동)
        dong_params = request.GET.get("dong")

        filters = []

        # 방종류 필터링
        if room_kind_params != None:
            filters.append(Q(room_kind=room_kind_params))

        # 매매종류 필터링
        if cell_kind_params != None:
            filters.append(Q(cell_kind=cell_kind_params))

        # 매매가 필터링
        if sale_start_params != None and sale_end_params != None:
            filters.append(Q(sale__range=(sale_start_params, sale_end_params)))

        # 보증금 필터링
        if deposit_start_params != None and deposit_end_params != None:
            filters.append(Q(deposit__range=(deposit_start_params, deposit_end_params)))

        # 월세 필터링
        if monthly_rent_start_params != None and monthly_rent_end_params != None:
            filters.append(
                Q(
                    monthly_rent__range=(
                        monthly_rent_start_params,
                        monthly_rent_end_params,
                    )
                )
            )

        # 관리비 필터링
        if (
            maintenance_cost_start_params != None
            and maintenance_cost_end_params != None
        ):
            filters.append(
                Q(
                    maintenance_cost__range=(
                        maintenance_cost_start_params,
                        maintenance_cost_end_params,
                    )
                )
            )

        # 방개수 필터링
        if num_of_room != None:
            if num_of_room == "1" or num_of_room == "2" or num_of_room == "3":
                filters.append(Q(room=num_of_room))
            else:
                filters.append(Q(room__gte=4))

        # 화장실개수 필터링
        if num_of_toilet != None:
            if num_of_toilet == "1" or num_of_toilet == "2" or num_of_toilet == "3":
                filters.append(Q(toilet=num_of_toilet))
            else:
                filters.append(Q(toilet__gte=4))

        # 평수 필터링
        if pyeongsu == "10":
            filters.append(Q(pyeongsu__range=(10, 19)))
        elif pyeongsu == "20":
            filters.append(Q(pyeongsu__range=(20, 29)))
        elif pyeongsu == "30":
            filters.append(Q(pyeongsu__range=(30, 39)))
        elif pyeongsu == "40":
            filters.append(Q(pyeongsu__gt=40))
        elif pyeongsu == "0":
            filters.append(Q(pyeongsu__range=(1, 9)))

        # 주소(서울시, 구, 동) 필터링
        if dong_params != None:
            filters.append(Q(dong=dong_params))

        if filters:
            house = House.objects.filter(*filters)
        else:
            house = House.objects.all()

        # 조회(최저가격순, 방문순, 최신순)
        sort_by = request.GET.get("sort_by")

        if sort_by == "row_price":
            house = house.order_by("price")
        elif sort_by == "visited":
            house = house.order_by("-visited")
        elif sort_by == "lastest":
            house = house.order_by("-created_at")

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

        # 조회 횟수
        house = self.get_object(pk)
        house.visited += 1
        house.save()
        serializer = serializers.HouseDetailSerializer(
            house,
        )

        # 조회 목록
        if request.user.is_authenticated:
            try:
                houselist = HouseList.objects.get(user=request.user)
            except HouseList.DoesNotExist:
                houselist = HouseList.objects.create(user=request.user)

            houselist.recently_views.add(house)
            houselist.save()
        else:
            raise ParseError("please login")

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
