from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_409_CONFLICT
from . import serializers
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from houses.models import House
from houses.serializers import TinyHouseSerializer
from django.core.paginator import Paginator


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
        serializer = serializers.PrivateUserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_user = serializer.save()
            serializer = serializers.PrivateUserSerializer(updated_user)
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
            refresh = RefreshToken.for_user(user)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)}
            )
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
            self.validate_password(password)
            user = serializer.save()
            if request.data.get("avatar"):
                user.avatar = request.data.get("avatar")
            user.set_password(password)
            # user.password = password 시에는 raw password로 저장
            user.save()
            # set_password 후 다시 저장
            serializer = serializers.PrivateUserSerializer(user)
            login(request, user)

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "data": serializer.data,
                },
                status=201,
            )
        else:
            return Response(serializer.errors, status=400)


class ChangePassword(APIView):
    def validate_password(self, password):
        REGEX_PASSWORD = "^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$"
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ParseError(
                "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 숫자, 특수문자로 구성되어야 하며 길이는 8자리 이상이어야 합니다."
            )

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
            self.validate_password(new_password)
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
    @swagger_auto_schema(
        operation_summary="중복 아이디 체크 api",
        responses={
            200: openapi.Response(
                description="Successful response",
            ),
            409: "Conflct Response",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="검사할 아이디",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def get(self, request):
        id = request.GET.get("id")
        if User.objects.filter(username=id).exists():
            return Response(status=HTTP_409_CONFLICT)
        return Response(status=200)


class CheckValidate(APIView):
    def validate_password(self, password):
        REGEX_PASSWORD = "^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$"
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ParseError(
                "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 숫자, 특수문자로 구성되어야 하며 길이는 8자리 이상이어야 합니다."
            )

    @swagger_auto_schema(
        operation_summary="회원가입 유효성 체크용 api",
        responses={
            200: openapi.Response(
                description="Successful response",
            ),
            400: "Bad request",
        },
        # request_body=serializers.PrivateUserSerializer(),
    )
    def post(self, request):
        password = str(request.data.get("password"))
        if not password:
            raise ParseError("password 가 입력되지 않았습니다.")

        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            self.validate_password(password)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


class KakaoLogin(APIView):
    @swagger_auto_schema(
        operation_summary="카카오 로그인 api",
        responses={
            200: openapi.Response(
                description="Successful response",
            ),
            201: openapi.Response(
                description="Create user ",
            ),
            400: "Bad request",
        },
        manual_parameters=[
            openapi.Parameter(
                name="code",
                in_=openapi.IN_QUERY,
                description="카카오톡에서 제공해주는 code",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = (
                requests.post(
                    "https://kauth.kakao.com/oauth/token",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={
                        "grant_type": "authorization_code",
                        "client_id": "69ba16ba77556c01d4a4ea9911fc06ad",
                        "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                        "code": code,
                    },
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                },
            ).json()
            # print(user_data)
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)

                return Response(status=200)
            except:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                    gender=kakao_account.get("gender"),
                    is_kakao=True,
                )
            user.set_unusable_password()
            user.save()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)},
                status=201,
            )
        except Exception as e:
            return Response(status=400)


class NaverLogin(APIView):
    @swagger_auto_schema(
        operation_summary="카카오 로그인 api",
        responses={
            200: openapi.Response(
                description="Successful response",
            ),
            201: openapi.Response(
                description="Create user ",
            ),
            400: "Bad request",
        },
        manual_parameters=[
            openapi.Parameter(
                name="code",
                in_=openapi.IN_QUERY,
                description="네이버에서 제공해주는 code",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def post(self, request):
        code = request.data.get("code")
        state = request.data.get("state")
        if state == "OzCoding":
            access_token = (
                requests.post(
                    "https://nid.naver.com/oauth2.0/token",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={
                        "grant_type": "authorization_code",
                        "client_id": "1Vm0j0Ggt3_VZer8jmHA",
                        "client_secret": "a4a3AQC1SB",
                        "code": code,
                        "state": state,
                    },
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()
            if (
                user_data.get("resultcode") == "00"
                and user_data.get("message") == "success"
            ):
                response = user_data.get("response")
                try:
                    user = User.objects.get(email=response.get("email"))
                    login(request, user)
                    return Response(status=200)
                except User.DoesNotExist:
                    user = User.objects.create(
                        username=response.get("id")[:10],
                        name=response.get("name"),
                        phone_number=response.get("mobile").replace("-", ""),
                        email=response.get("email"),
                        gender="male" if response.get("gender") == "M" else "female",
                        avatar=response.get("profile_image"),
                        is_naver=True,
                    )
                    user.set_unusable_password()
                    user.save()
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {"access": str(refresh.access_token), "refresh": str(refresh)},
                        status=201,
                    )

            return Response(status=400)


class AllSellList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="유저가 올린 모든방의 리스트를 보여주는 api",
        produces=["application/json"],
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "num_pages": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Number of pages",
                        ),
                        "current_page": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Current page number",
                        ),
                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total number of houses",
                        ),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="House ID",
                                    ),
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="House title",
                                    ),
                                    "thumbnail": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_URI,
                                        description="House thumbnail URL",
                                    ),
                                    "room_kind": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Type of room",
                                    ),
                                    "deposit": openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        format=openapi.FORMAT_FLOAT,
                                        description="Deposit amount",
                                    ),
                                    "sell_kind": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Type of sale",
                                    ),
                                    "sale": openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description="Whether the house is for sale",
                                    ),
                                    "monthly_rent": openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        format=openapi.FORMAT_FLOAT,
                                        description="Monthly rent amount",
                                    ),
                                },
                            ),
                            description="Houses for sale",
                        ),
                    },
                ),
            ),
            403: "permission denied",
        },
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request):
        if not request.user.is_host:
            raise PermissionDenied
        house = House.objects.filter(host=request.user)
        current_page = request.GET.get("page", 1)
        items_per_page = 24
        paginator = Paginator(house, items_per_page)
        try:
            page = paginator.page(current_page)
        except:
            page = paginator.page(paginator.num_pages)

        serializer = TinyHouseSerializer(
            page,
            many=True,
            context={"request": request},
        )

        data = {
            "num_pages": paginator.num_pages,
            "current_page": page.number,
            "count": paginator.count,
            "results": serializer.data,
        }
        return Response(data)


class NotSellList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="유저가 올린 방 중 이미 팔린 방의 리스트를 보여주는 api",
        produces=["application/json"],
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "num_pages": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Number of pages",
                        ),
                        "current_page": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Current page number",
                        ),
                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total number of houses",
                        ),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="House ID",
                                    ),
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="House title",
                                    ),
                                    "thumbnail": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_URI,
                                        description="House thumbnail URL",
                                    ),
                                    "room_kind": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Type of room",
                                    ),
                                    "deposit": openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        format=openapi.FORMAT_FLOAT,
                                        description="Deposit amount",
                                    ),
                                    "sell_kind": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Type of sale",
                                    ),
                                    "sale": openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description="Whether the house is for sale",
                                    ),
                                    "monthly_rent": openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        format=openapi.FORMAT_FLOAT,
                                        description="Monthly rent amount",
                                    ),
                                },
                            ),
                            description="Houses for sale",
                        ),
                    },
                ),
            ),
            403: "permission denied",
        },
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request):
        if not request.user.is_host:
            raise PermissionDenied
        house = House.objects.filter(host=request.user, is_sale=False)
        current_page = request.GET.get("page", 1)
        items_per_page = 24
        paginator = Paginator(house, items_per_page)
        try:
            page = paginator.page(current_page)
        except:
            page = paginator.page(paginator.num_pages)

        serializer = TinyHouseSerializer(
            page,
            many=True,
            context={"request": request},
        )

        data = {
            "num_pages": paginator.num_pages,
            "current_page": page.number,
            "count": paginator.count,
            "results": serializer.data,
        }
        return Response(data)


class SellList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="유저가 올린 방중 파는중인 방의 리스트를 보여주는 api",
        produces=["application/json"],
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "num_pages": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Number of pages",
                        ),
                        "current_page": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Current page number",
                        ),
                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total number of houses",
                        ),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="House ID",
                                    ),
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="House title",
                                    ),
                                    "thumbnail": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_URI,
                                        description="House thumbnail URL",
                                    ),
                                    "room_kind": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Type of room",
                                    ),
                                    "deposit": openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        format=openapi.FORMAT_FLOAT,
                                        description="Deposit amount",
                                    ),
                                    "sell_kind": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Type of sale",
                                    ),
                                    "sale": openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description="Whether the house is for sale",
                                    ),
                                    "monthly_rent": openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        format=openapi.FORMAT_FLOAT,
                                        description="Monthly rent amount",
                                    ),
                                },
                            ),
                            description="Houses for sale",
                        ),
                    },
                ),
            ),
            403: "permission denied",
        },
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request):
        if not request.user.is_host:
            raise PermissionDenied
        house = House.objects.filter(host=request.user, is_sale=True)
        current_page = request.GET.get("page", 1)
        items_per_page = 24
        paginator = Paginator(house, items_per_page)
        try:
            page = paginator.page(current_page)
        except:
            page = paginator.page(paginator.num_pages)

        serializer = TinyHouseSerializer(
            page,
            many=True,
            context={"request": request},
        )

        data = {
            "num_pages": paginator.num_pages,
            "current_page": page.number,
            "count": paginator.count,
            "results": serializer.data,
        }
        return Response(data)
