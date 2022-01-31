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

class UserloginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email', 'username', 'provider']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            provider=validated_data['provider'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
