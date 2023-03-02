from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers
from .models import House


class Houses(APIView):
    def get(self, request):
        room_params = request.query_params.get("room_kind")
        cell_params = request.query_params.get("cell_kind")
        if room_params != None or cell_params != None:
            if room_params != None and cell_params != None:
                house = House.objects.filter(
                    room_kind=room_params, cell_kind=cell_params
                )
                print(1)
            elif room_params != None and cell_params == None:
                house = House.objects.filter(room_kind=room_params)
                print(2)

            elif room_params == None and cell_params != None:
                house = House.objects.filter(cell_kind=cell_params)
                print(3)

        else:
            house = House.objects.all()

        serializer = serializers.HouseSerializer(
            house,
            many=True,
        )
        return Response(serializer.data)


class HouseDetail(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        house = self.get_object(pk)
        house.visited += 1
        house.save()
        serializer = serializers.HouseDetailSerializer(house)
        return Response(serializer.data)
