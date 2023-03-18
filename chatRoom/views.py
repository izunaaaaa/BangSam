from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatListSerializer, ChatRoomListSerializer, ChatRoomSerialzier
from houses.models import House

# Create your views here.
class ChattingRoomList(APIView):

    permission_classes = [IsAuthenticated]

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

    def get(self, request, pk):
        chatRoom = self.get_object(pk)
        serializer = ChatRoomListSerializer(
            chatRoom,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request, pk):
        house = self.get_house(pk)
        serializer = ChatRoomSerialzier(data=request.data)
        if serializer.is_valid():
            if ChatRoom.objects.filter(
                house=house, users__in=[request.user, house.host]
            ).exists():
                return Response({"Already Exist"})
            chat_room = serializer.save(house=house)
            chat_room.users.add(request.user)
            chat_room.users.add(house.host)
            serializer = ChatRoomSerialzier(chat_room)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        chatRoom = self.get_object(pk)
        chatRoom.delete()
        return Response({"Ok"}, status=200)


class ChattingList(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            raise NotFound

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
