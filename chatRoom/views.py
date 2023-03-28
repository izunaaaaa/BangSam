from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatListSerializer, ChatRoomListSerializer, ChatRoomSerialzier
from houses.models import House
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class ChattingRoomList(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="유저의 채팅방 리스트를 보여주는 api",
        responses={
            200: openapi.Response(
                description="Succfull Response",
                schema=ChatRoomListSerializer(many=True),
            )
        },
    )
    def get(self, request):
        all_chat_list = ChatRoom.objects.filter(users=request.user).order_by(
            "-updated_at"
        )
        serializer = ChatRoomListSerializer(
            all_chat_list,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


class ChattingRoom(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            raise NotFound

    def get_house(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="채팅방 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=ChatRoomListSerializer(),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def get(self, request, pk):
        chatRoom = self.get_object(pk)
        serializer = ChatRoomListSerializer(
            chatRoom,
            context={"request": request},
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="채팅방 생성 api",
        request_body=openapi.Schema(
            type="None",
            properties={},
        ),
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=ChatRoomListSerializer(),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def post(self, request, pk):
        house = self.get_house(pk)
        serializer = ChatRoomSerialzier(data=request.data)
        if serializer.is_valid():
            if (
                ChatRoom.objects.filter(house=house)
                .filter(users__in=[request.user])
                .filter(users__in=[house.host])
                .exists()
            ):
                room = (
                    ChatRoom.objects.filter(house=house)
                    .filter(users__in=[request.user])
                    .filter(users__in=[house.host])
                )[0]

                # print(room.users.all())
                return Response({"id": room.id})
            chat_room = serializer.save(house=house)
            chat_room.users.add(request.user)
            chat_room.users.add(house.host)
            serializer = ChatRoomSerialzier(chat_room)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="채팅방 삭제 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def delete(self, request, pk):
        chatRoom = self.get_object(pk)
        chatRoom.delete()
        return Response("Ok", status=200)


class ChattingList(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="특정 채팅방의 채팅내역을 가져오는 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=ChatListSerializer(many=True),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def get(self, request, pk):
        room = self.get_object(pk)
        if request.user in room.users.all():
            msg = Message.objects.filter(room=room).reverse()
            msg.exclude(sender=request.user).update(is_read=True)
            serializer = ChatListSerializer(
                msg,
                many=True,
            )
            return Response(serializer.data)
        else:
            raise PermissionDenied
