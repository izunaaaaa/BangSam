from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import HouseList
from .serializers import HouseListSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class HouseLists(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="요청한 유저의 최근 본 방 목록을 가져오는 api (최대 10개)",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=HouseListSerializer(many=True),
            ),
        },
    )
    def get(self, request):
        houselist = HouseList.objects.filter(user=request.user)
        serailizer = HouseListSerializer(houselist, many=True)
        return Response(serailizer.data)
