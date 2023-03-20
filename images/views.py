from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetUploadURL(APIView):
    @swagger_auto_schema(
        operation_summary="이미지 업로드용 URL 요청 API",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type="object",
                    properties={"uploadURL": openapi.Schema(type="string")},
                ),
            ),
        },
    )
    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
            },
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result").get("uploadURL")
        return Response({"uploadURL": result})
