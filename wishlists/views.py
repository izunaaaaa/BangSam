from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from . import serializers
from .models import Wishlist
from houses.serializers import TinyHouseSerializer

class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            raise NotFound
        house = wishlist.house.all()
        serializer = TinyHouseSerializer(house,many=True)
        return Response(serializer.data)
    