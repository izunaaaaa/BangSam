from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import Review


class Reviews(APIView):
    def get(self, request):
        review = Review.objects.all()
        serializer = serializers.ReviewSerializer(review, many=True)
        return Response(serializer.data)
