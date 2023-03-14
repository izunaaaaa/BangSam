from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
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
    def get(self, reqeust):
        wishlist = Wishlist.objects.filter(user=reqeust.user)
        serializer = serializers.WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            house = serializers.save(user=request.user)
            return Response(WishlistSerializer(house).data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Wishlist.objects.get(pk=pk)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk)
        serializers = serializers.WishlistSerializer(wishlist)
        return Response(serializers.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk).delete()
        return wishlist
