from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
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
    def get(self, request):
        all_wishlist = Wishlist.objects.filter(user=request.user)
        serilaizer = serializers.WishlistSerializer(
            all_wishlist,
            many=True,
        )

        return Response(serilaizer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_onject(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)
