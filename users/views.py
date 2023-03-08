from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from . import serializers
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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


class LogIn(APIView):
    @swagger_auto_schema(
        operation_summary="유저 로그인 api",
        responses={200: "OK", 400: "Not Found"},
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"}, status=400)
