from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import House, Gu_list, Dong_list
from . import serializers
from houselists.models import HouseList


class Houses(APIView):
    @swagger_auto_schema(
        operation_summary="모든 방에 대한 리스트를 가져오는 api",
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="1 페이지당 24개의 데이터 : num_pages(총 페이지수),current_page(현재 페이지),count(총 개수),results(순서)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "room_kind",
                openapi.IN_QUERY,
                description="방종류 : ONE_ROOM, HOME, APART, VILLA, OFFICETEL, SHARE_HOUSE ",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "sell_kind",
                openapi.IN_QUERY,
                description="매매종류 : SALE, CHARTER, MONTHLY_RENT ",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "sale_start",
                openapi.IN_QUERY,
                description="매매가 최소금액(default=0)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "sale_end",
                openapi.IN_QUERY,
                description="매매가 최대금액(default=0)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "deposit_start",
                openapi.IN_QUERY,
                description="보증금 최소금액(default=0)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "deposit_end",
                openapi.IN_QUERY,
                description="보증금 최대금액(default=0)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "monthly_rent_start",
                openapi.IN_QUERY,
                description="월세 최소금액(default=0)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "monthly_rent_end",
                openapi.IN_QUERY,
                description="월세 최대금액(default=0)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "maintenance_cost_start",
                openapi.IN_QUERY,
                description="관리비 최소금액(default=0)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "maintenance_cost_end",
                openapi.IN_QUERY,
                description="관리비 최대금액(default=0)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "num_of_room",
                openapi.IN_QUERY,
                description="방개수 : 1(1개), 2(2개), 3(3개), 4 (4개이상)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "num_of_toilet",
                openapi.IN_QUERY,
                description="화장실 개수 : 1(1개), 2(2개), 3(3개), 4 (4개이상)",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "pyeongsu",
                openapi.IN_QUERY,
                description="평수 : 10(10, 19), 20(20, 29), 30(30, 39), 40(40, 49), 50(pyeongsu__gt=50), 0(1-9)",
                type=openapi.TYPE_INTEGER,
            ),
            # openapi.Parameter(
            #     "gu",
            #     openapi.IN_QUERY,
            #     description="구",
            #     type=openapi.TYPE_INTEGER,
            # ),
            openapi.Parameter(
                "dong",
                openapi.IN_QUERY,
                description="동",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "sort_by",
                openapi.IN_QUERY,
                description="row_price, visited, lastest",
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

        # 방종류
        room_kind = request.GET.get("room_kind")

        # 매매종류
        sell_kind = request.GET.get("sell_kind")

        # 매매가
        sale_start = request.GET.get("sale_start")
        sale_end = request.GET.get("sale_end")

        # 보증금
        deposit_start = request.GET.get("deposit_start")
        deposit_end = request.GET.get("deposit_end")

        # 월세
        monthly_rent_start = request.GET.get("monthly_rent_start")
        monthly_rent_end = request.GET.get("monthly_rent_end")

        # 관리비
        maintenance_cost_start = request.GET.get("maintenance_cost_start")
        maintenance_cost_end = request.GET.get("maintenance_cost_end")

        # 방개수
        num_of_room = request.GET.get("num_of_room")

        # 화장실개수
        num_of_toilet = request.GET.get("num_of_toilet")

        # 평수
        pyeongsu = request.GET.get("pyeongsu")

        # 주소 : 동
        dong = request.GET.get("dong")

        filters = []
        # 방종류 필터링
        if room_kind != None:
            filters.append(Q(room_kind=room_kind))

        # 매매종류 필터링
        if sell_kind != None:
            filters.append(Q(sell_kind=sell_kind))

        # 매매가 필터링
        if sale_start != None and sale_end != None:
            filters.append(Q(sale__range=(sale_start, sale_end)))

        # 보증금 필터링
        if deposit_start != None and deposit_end != None:
            filters.append(Q(deposit__range=(deposit_start, deposit_end)))

        # 월세 필터링
        if monthly_rent_start != None and monthly_rent_end != None:
            filters.append(
                Q(
                    monthly_rent__range=(
                        monthly_rent_start,
                        monthly_rent_end,
                    )
                )
            )

        # 관리비 필터링
        if maintenance_cost_start != None and maintenance_cost_end != None:
            filters.append(
                Q(
                    maintenance_cost__range=(
                        maintenance_cost_start,
                        maintenance_cost_end,
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
            filters.append(Q(pyeongsu__range=(40, 49)))
        elif pyeongsu == "50":
            filters.append(Q(pyeongsu__gt=50))
        elif pyeongsu == "0":
            filters.append(Q(pyeongsu__range=(1, 9)))

        filters.append(Q(is_sale=True))

        # 동 필터링
        if dong != None:
            filters.append(Q(dong=dong))

        if filters:
            house = House.objects.filter(*filters)
        else:
            house = House.objects.filter(is_sale=True)

        # # 주소 구
        # gu = request.GET.get("gu")
        # if gu:
        #     try:
        #         gu = Gu_list.objects.get(pk=gu).name
        #         house = [i for i in house if i.gu == gu]
        #     except:
        #         raise NotFound

        # 조회(최저가격순, 방문순, 최신순)
        sort_by = request.GET.get("sort_by")

        if sort_by == "row_price":
            if sell_kind == "SALE":
                house = house.order_by("sale")
            if sell_kind == "CHARTER":
                house = house.order_by("deposit")
            if sell_kind == "MONTHLY_RENT":
                house = house.order_by("monthly_rent")
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

        return Response(data)

    def post(self, request):

        serializer = serializers.HouseSerializer(data=request.data)

        if serializer.is_valid():

            room = request.data.get("room")
            if room == None:
                raise ParseError("room not specified")

            toilet = request.data.get("toilet")
            if toilet == None:
                raise ParseError("toilet not specified")

            pyeongsu = request.data.get("pyeongsu")
            if pyeongsu == None:
                raise ParseError("pyeongsu not specified")

            sell_kind = request.data.get("sell_kind")
            if sell_kind == "SALE":
                if (
                    request.data.get("sale") == 0
                    or request.data.get("sale") == None
                    or request.data.get("deposit")
                    or request.data.get("monthly_rent")
                ):
                    raise ParseError("sale error")

            if sell_kind == "CHARTER":
                if (
                    request.data.get("deposit") == 0
                    or request.data.get("deposit") == None
                    or request.data.get("sale")
                    or request.data.get("monthly_rent")
                ):
                    raise ParseError("deposit error")

            if sell_kind == "MONTHLY_RENT":
                if (
                    request.data.get("monthly_rent") == 0
                    or request.data.get("monthly_rent") == None
                    or request.data.get("deposit")
                    or request.data.get("monthly_rent")
                ):
                    raise ParseError("monthly_rent error")

            house = serializer.save(
                host=request.user,
                room=room,
                toilet=toilet,
                pyeongsu=pyeongsu,
                sell_kind=sell_kind,
            )
            serializer = serializers.HouseSerializer(house)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        House.objects.all().delete()
        return Response({"delete success"})


class HouseDetail(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

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
    def get_object(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise NotFound

    def get(self, request, pk):

        # 조회 횟수
        house = self.get_object(pk)
        house.visited += 1

        # 유저인지 확인
        if request.user == house.host:
            house.is_host = True
        else:
            house.is_host = False

        house.save()

        # 조회 목록
        if request.user.is_authenticated:

            try:
                houselist = HouseList.objects.get(recently_views=house)
                houselist.updated_at = timezone.now()

            except HouseList.DoesNotExist:
                houselist = HouseList.objects.create(
                    user=request.user,
                    recently_views=house,
                )

        serializer = serializers.HouseDetailSerializer(house)

        return Response(serializer.data)

    def put(self, request, pk):
        house = self.get_object(pk)

        if house.host != request.user:
            raise PermissionDenied

        serializer = serializers.HouseDetailSerializer(
            house,
            data=request.data,
            partial=True,
        )

        print(house.sell_kind)

        if serializer.is_valid():

            # sell_kind = request.data.get("sell_kind")
            # if sell_kind == "SALE":
            #     if (
            #         request.data.get("sale") == 0
            #         or request.data.get("sale") == None
            #         or request.data.get("deposit")
            #         or request.data.get("monthly_rent")
            #     ):
            #         raise ParseError("sale error")

            # if sell_kind == "CHARTER":
            #     if (
            #         request.data.get("deposit") == 0
            #         or request.data.get("deposit") == None
            #         or request.data.get("sale")
            #         or request.data.get("monthly_rent")
            #     ):
            #         raise ParseError("deposit error")

            # if sell_kind == "MONTHLY_RENT":
            #     if (
            #         request.data.get("monthly_rent") == 0
            #         or request.data.get("monthly_rent") == None
            #         or request.data.get("deposit")
            #         or request.data.get("monthly_rent")
            #     ):
            #         raise ParseError("monthly_rent error")

            updated_house = serializer.save()
            serializer = serializers.HouseDetailSerializer(updated_house)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        house = self.get_object(pk)

        if house.host != request.user:
            raise PermissionDenied
        house.delete()
        return Response({"delete success"})


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
