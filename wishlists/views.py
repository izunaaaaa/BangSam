from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, ParseError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from houses.serializers import TinyHouseSerializer
from .models import Wishlist
from houses.models import House
from . import serializers


class Wishlists(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

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
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = serializers.WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        house_pk = request.data.get("house_pk")
        if not house_id:
            raise ParseError("house_pk is required")
        wishlist = Wishlist.objects.get(pk=house_pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
