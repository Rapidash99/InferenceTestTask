from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Message, User
from .permissions import (IsSender, IsSenderOrReadOnlyReceiver,
                          IsSenderOrReceiver)
from .serializers import (MessageCreateSerializer, MessageListSerializer,
                          MessageTextSerializer, UserAllSerializer)


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = (IsAuthenticated, )


class MessageListView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    queryset = Message.objects.all()
    permission_classes = (IsSenderOrReceiver, )

    def get_queryset(self):
        return self.queryset.filter(Q(receiver_id=self.request.user.id) | Q(sender_id=self.request.user.id))


class MessageListByUserView(generics.ListAPIView):
    serializer_class = MessageListSerializer
    queryset = Message.objects.all()
    permission_classes = (IsSenderOrReceiver, )

    def get_queryset(self):
        # if by username:
        if self.kwargs.__contains__('username'):
            who = self.request.user.username
            whom = self.kwargs['username']

            return self.queryset.filter((Q(sender__username=whom) & Q(receiver__username=who)) |
                                        (Q(sender__username=who) & Q(receiver__username=whom)))
        # else if by user id
        else:
            who = self.request.user.id
            whom = self.kwargs['pk']

            return self.queryset.filter((Q(sender_id=whom) & Q(receiver_id=who)) |
                                        (Q(sender_id=who) & Q(receiver_id=whom)))


class MessageDetailedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageTextSerializer
    queryset = Message.objects.all()
    permission_classes = (IsSenderOrReadOnlyReceiver, )

    # if text was changed via 'put' or 'patch', set 'edited' as True
    def put(self, request, *args, **kwargs):
        msg = self.queryset.get(id=self.kwargs['pk'])
        new_text = self.request.data.get('text')

        if new_text != msg.text:
            msg.edited = True
            msg.save(update_fields=['edited'])

        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        msg = self.queryset.get(id=self.kwargs['pk'])
        new_text = self.request.data.get('text')

        if new_text != msg.text:
            msg.edited = True
            msg.save(update_fields=['edited'])

        return self.partial_update(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    serializer_class = UserAllSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, )
