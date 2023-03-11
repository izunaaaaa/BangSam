from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HouseList
from . import serializers


class HouseLists(APIView):
    def get(self, request):
        houselist = HouseList.objects.filter(user=request.user)
        serailizer = serializers.HouseListSerializer(houselist, many=True)
        return Response(serailizer.data)
