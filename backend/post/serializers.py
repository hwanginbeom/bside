#backend/post/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'nickname',
        )


class MeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = (
            'user_id',
            'meet_id',
            'meet_title',
            'meet_date',
            'status',
            'participants',
            'goal',
            'last_time',
        )


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = (
            'meet_id',
            'agenda_id',
            'agenda_title',
            'discussion',
            'decisions',
            'setting_time',
            'progress_time',
        )


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = (
            'agenda_id',
            'action_id',
            'action_title',
            'person',
            'dead_line',
        )


User = get_user_model()

class UsercreateSerializer(serializers.Serializer):
    # email = serializers.CharField(max_length=200, required=True)
    # username = serializers.CharField(max_length=200, required=False)
    # nickname = serializers.CharField(max_length=200, required=False)
    # password = serializers.CharField(max_length=200, required=False)
    # provider = serializers.CharField(max_length=200, required=False)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            provider=validated_data['provider'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
        )
        user.save()
        return user
#
class UserloginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'username', 'provider', 'nickname']
    # password = serializers.CharField(max_length=200, required=False)
    # email = serializers.CharField(max_length=200, required=True)
    # username = serializers.CharField(max_length=200, required=False)
    # provider = serializers.CharField(max_length=200, required=False)
    # nickname = serializers.CharField(max_length=200, required=False)
