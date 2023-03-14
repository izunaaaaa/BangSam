from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, ParseError
from . import serializers
from .models import Wishlist
from houses.serializers import TinyHouseSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Wishlists(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="요청한 유저의 wishlist 를 가져오는 api",
        responses={200: "OK", 404: "Not Found"},
    )
    def get(self, request, pk):
        wishlist = self.get_object(pk)
        serializers = serializers.WishlistSerializer(wishlist)
        return Response(serializers.data)

    def post(self, request, pk):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            house_pk = request.data.get("house_pk")
            if not house_pk:
                raise ParseError("house_pk is required")
            try:
                house_pk = Wishlist.objects.get(pk=house_pk)
            except Wishlist.DoesNotExist:
                raise ParseError("house_pk is invalid")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk).delete()
        return wishlist
