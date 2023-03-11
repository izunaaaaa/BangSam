from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests

# Create your views here.
class GetUploadURL(APIView):
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
