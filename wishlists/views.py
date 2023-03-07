from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from . import serializers
from .models import Wishlist
from houses.serializers import TinyHouseSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="요청한 유저의 wishlist 를 가져오는 api",
        responses={200: "OK", 404: "Not Found"},
    )
    def get(self, request):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            raise NotFound
        house = wishlist.house.all()
        serializer = TinyHouseSerializer(house, many=True)
        return Response(serializer.data)
