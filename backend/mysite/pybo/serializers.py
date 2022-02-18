# backend/post/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'name',
            'nickname',
            'provider',
            'last_login',
            'img',
        )


class MeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = (
            'email',
            'meet_id',
            'meet_title',
            'meet_date',
            'meet_status',
            'rm_status',
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
            'agenda_status',
            'discussion',
            'decisions',
            'setting_time',
            'progress_time',
            'order_number',
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


class SelfCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfCheck
        fields = (
            'meet_id',
            'check_id',
            'ownership',
            'participation',
            'efficiency',
            'productivity',
        )


# 유저 db저장
class UsersaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email', 'name', 'img', 'provider']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            provider=validated_data['provider'],
            img=validated_data['img'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserchkSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']
    # email = serializers.CharField(max_length=200)

    def validate(self, data):
        email = data.get('email', None)
        # password = data.get('password', None)
        user = authenticate(email=email)

        if user is None:
            return {
                'email': 'None'
            }


# 유저 로그인 진행
User_auth = get_user_model()

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserloginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200, write_only=True)
    name = serializers.CharField(max_length=200)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except user.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exist'
            )

        return {'token': token}

