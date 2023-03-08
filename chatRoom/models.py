from django.db import models
from common.models import CommonModel
from django.utils import timezone

# Create your models here.
class ChatRoomManager(models.Manager):
    def delete_inactive_rooms(self):
        # delete chat rooms that have not been active for more than 3 months
        oldest_allowed_last_activity = timezone.now() - timezone.timedelta(days=90)
        self.filter(last_activity__lt=oldest_allowed_last_activity).delete()


class ChatRoom(CommonModel):
    users = models.ManyToManyField(
        "users.User",
        related_name="chatRoom",
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="chat room",
    )
    # last_activity = models.DateTimeField(default=timezone.now)

    @property
    def lastMessage(self):
        if self.messages.exists():
            return self.messages.order_by("-created_at").first().text
        else:
            return "메세지가 없습니다."

    # def update_last_activity(self):
    #     # update the last activity timestamp of the chat room to the current time
    #     self.last_activity = timezone.now()
    #     self.save()

    def __str__(self) -> str:
        return str(self.pk) + "'st " + self.name


class Message(CommonModel):
    text = models.TextField()
    # room = models.ForeignKey("rooms.")
    sender = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="send_messages",
    )
    room = models.ForeignKey(
        "chatRoom.ChatRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    is_read = models.BooleanField(default=False)
    sequence_number = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["room", "sequence_number"]

    # def __str__(self) -> str:
    # return f"{self.sender.name} to {self.room} : {self.text}"

    def save(self, *args, **kwargs):
        # set the sequence number of the new message to the highest sequence number in the chat room plus one
        self.sequence_number = (
            self.room.messages.aggregate(models.Max("sequence_number"))[
                "sequence_number__max"
            ]
            or 0
        )
        self.sequence_number += 1

        # delete old messages if there are more than 100 messages in the chat room
        max_messages = 100
        num_messages = self.room.messages.count()
        if num_messages >= max_messages:
            # find the oldest messages and delete them
            messages_to_delete = self.room.messages.order_by("sequence_number")[
                : num_messages - max_messages + 1
            ]
            for message in messages_to_delete:
                message.delete()

        # update the last activity timestamp of the chat room to the current time
        # self.room.update_last_activity()
        self.room.updated_at = timezone.now()
        self.room.save(update_fields=["updated_at"])

        super(Message, self).save(*args, **kwargs)
