from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import User


class Users(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.all()
        serializer = serializers.UserSerializer(user, many=True)
        return Response(serializer.data)


class UserMe(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user = User.objects.get(pk=request.user.id)
        user = request.user
        serilaizer = serializers.UserSerializer(user)
        return Response(serilaizer.data)


class UserDetail(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            raise NotFound
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
