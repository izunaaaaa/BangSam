from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from houses.serializers import TinyHouseSerializer
from .models import Wishlist
from houses.models import House
from . import serializers


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="요청한 유저의 wishlist 를 가져오는 api",
        responses={200: "OK", 404: "Not Found"},
    )
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = serializers.WishlistSerializer(
            wishlist,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WishlistSerializer(data=request.data)
        if serializer.is_valid():
            if Wishlist.objects.filter(
                user=request.user, house=request.data.get("house")
            ).exists():
                Wishlist.objects.filter(
                    user=request.user, house=request.data.get("house")
                ).delete()
                return Response({"result": "delete success"})
            else:
                wishlist = serializer.save(
                    user=request.user,
                )
                serializer = serializers.WishlistSerializer(wishlist)
                return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)
