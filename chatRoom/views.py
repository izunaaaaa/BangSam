from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import ChatRoom, Message
from .serializers import ChatListSerializer, ChatRoomListSerializer

# Create your views here.
class ChattingRoomList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_chat_list = ChatRoom.objects.filter(users=request.user)
        serializer = ChatRoomListSerializer(
            all_chat_list,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


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
