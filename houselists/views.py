from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import HouseList
from .serializers import HouseListSerializer


class HouseLists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        houselist = HouseList.objects.filter(user=request.user)
        serailizer = HouseListSerializer(houselist, many=True)
        return Response(serailizer.data)
