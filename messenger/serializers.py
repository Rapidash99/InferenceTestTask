from rest_framework import serializers

from .models import Message, User


class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sent', 'edited']


class MessageListSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField('sender_name')
    receiver_username = serializers.SerializerMethodField('receiver_name')

    def sender_name(self, message):
        return message.sender.username

    def receiver_name(self, message):
        return message.receiver.username

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender']


class MessageTextSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField('sender_name')
    receiver_username = serializers.SerializerMethodField('receiver_name')

    def sender_name(self, message):
        return message.sender.username

    def receiver_name(self, message):
        return message.receiver.username

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'receiver', 'sent', 'edited']


class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
