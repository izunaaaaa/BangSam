from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_409_CONFLICT
from . import serializers
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re


class UserMe(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="요청한 유저의 정보를 가져오는 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.PrivateUserSerializer(),
            ),
        },
    )
    def get(self, request):
        # user = User.objects.get(pk=request.user.id)
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="요청한 유저의 정보를 수정하는 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.PrivateUserSerializer(),
            ),
            400: "Bad Request",
        },
        request_body=serializers.PrivateUserSerializer(),
    )
    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class UserDetail(APIView):
    @swagger_auto_schema(
        operation_summary="특정 유저의 정보를 가져오는 api",
        # responses={200: "OK", 404: "Not Found"},
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.TinyUserSerializer(),
            ),
            404: openapi.Response(
                description="User not found",
            ),
        },
    )
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            raise NotFound
        serializer = serializers.TinyUserSerializer(user)
        return Response(serializer.data)


class LogIn(APIView):
    @swagger_auto_schema(
        operation_summary="유저 로그인 api",
        responses={200: "OK", 400: "name or password error"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저 id ( username )"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저 비밀번호"
                ),
            },
        ),
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
            return Response({"error": "wrong name or password"}, status=400)


class SignUp(APIView):
    def validate_password(self, password):
        REGEX_PASSWORD = "^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$"
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ParseError(
                "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 숫자, 특수문자로 구성되어야 하며 길이는 8자리 이상이어야 합니다."
            )

    @swagger_auto_schema(
        operation_summary="회원가입 api",
        responses={
            201: "Created",
            400: "bad request",
        },
        request_body=serializers.PrivateUserSerializer(),
    )
    def post(self, request):
        password = str(request.data.get("password"))
        if not password:
            raise ParseError("password 가 입력되지 않았습니다.")

        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.validate_password(password)
            user.set_password(password)
            # user.password = password 시에는 raw password로 저장
            user.save()
            # set_password 후 다시 저장
            serializer = serializers.PrivateUserSerializer(user)
            login(request, user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="비밀번호 수정 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["old_password", "new_password"],
            properties={
                "old_password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="현재 비밀번호 입력"
                ),
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="새로운 비밀번호 입력"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
            401: openapi.Response(description="The user is not authenticated"),
        },
    )
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError("Invalid password")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=200)
        else:
            return Response(status=400)


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="로그아웃 api",
        operation_description="로그아웃",
        responses={200: "OK", 403: "Forbidden"},
    )
    def post(self, request):
        logout(request)
        return Response({"LogOut": True})


class CheckID(APIView):
    def get(self, request):
        id = request.GET.get("id")
        if User.objects.filter(username=id).exists():
            return Response(status=HTTP_409_CONFLICT)


class CheckValidate(APIView):
    def validate_password(self, password):
        REGEX_PASSWORD = "^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$"
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ParseError(
                "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 숫자, 특수문자로 구성되어야 하며 길이는 8자리 이상이어야 합니다."
            )

    def post(self, request):
        password = str(request.data.get("password"))
        if not password:
            raise ParseError("password 가 입력되지 않았습니다.")

        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
