from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import Review
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Reviews(APIView):
    @swagger_auto_schema(
        operation_summary="모든 리뷰를 가져오는 api",
        responses={200: "OK"},
    )
    def get(self, request):
        review = Review.objects.all()
        serializer = serializers.ReviewSerializer(review, many=True)
        return Response(serializer.data)
