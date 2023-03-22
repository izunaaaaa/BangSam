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

    def get_object(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="요청한 유저의 wishlist 를 가져오는 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.WishlistSerializer(many=True),
            ),
            404: "Not Found",
        },
    )
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = serializers.WishlistSerializer(
            wishlist,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="요청한 유저의 wishlist 에 추가 / 삭제하는 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["house"],
            properties={
                "house": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="wishlist 에 추가 / 삭제 할 방의 pk",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Successful Response",
            ),
            404: "Not Found",
        },
    )
    def post(self, request):
        house = self.get_object(request.data.get("house"))
        serializer = serializers.WishlistSerializer(data=request.data)
        if serializer.is_valid():
            if Wishlist.objects.filter(
                user=request.user,
                house=house,
            ).exists():
                Wishlist.objects.filter(
                    user=request.user,
                    house=house,
                ).delete()
                return Response({"result": "delete success"})
            else:
                wishlist = serializer.save(
                    user=request.user,
                    house=house,
                )
                serializer = serializers.WishlistSerializer(wishlist)
                return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)


class Isliked(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        house = self.get_object(pk)
        return Wishlist.objects.filter(
            user=request.user,
            house=house,
        ).exists()
