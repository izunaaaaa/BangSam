from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from . import serializers
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Users(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="모든 유저 리스트를 api",
        responses={200: "OK"},
    )
    def get(self, request):
        user = User.objects.all()
        serializer = serializers.UserSerializer(user, many=True)
        return Response(serializer.data)


class UserMe(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="요청한 유저의 정보를 가져오는 api",
        responses={200: "OK"},
    )
    def get(self, request):
        # user = User.objects.get(pk=request.user.id)
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


class UserDetail(APIView):
    @swagger_auto_schema(
        operation_summary="특정 유저의 정보를 가져오는 api",
        responses={200: "OK", 404: "Not Found"},
    )
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            raise NotFound
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
