from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Houselist
from . import serializers


class HouseLists(APIView):
    def get(self, request):
        houselist = Houselist.objects.all()
        serailizer = serializers.HouseListSerializer(
            houselist,
            many=True,
        )
        return Response(serailizer.data)
