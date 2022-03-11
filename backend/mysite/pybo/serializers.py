# backend/post/serializers.py
from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings
from datetime import datetime, timedelta
from .models import *


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=200, required=False)
    password = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'name',
            'nickname',
            'provider',
            'last_login',
            'img',
            'join_date',
        )


class MeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = (
            'user_id',
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


class ProgressSerializer(serializers.ModelSerializer):
    agenda_id = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Agenda_progress
        fields = (
            'agenda_id',
            'progress_id',
            'progress_time',
        )

    def create(self, validated_data):
        agenda_id = Agenda.objects.get(agenda_id=validated_data['agenda_id'])
        progress_time = ""
        if "progress_time" in validated_data:
            progress_time = validated_data['progress_time']

        progress = Agenda_progress.objects.create(
            agenda_id=agenda_id,
            progress_time=progress_time
        )
        return progress


class ActionSerializer(serializers.ModelSerializer):
    agenda_id = serializers.CharField(max_length=200, required=False)
    action_title = serializers.CharField(max_length=200, required=False, allow_blank=True)
    person = serializers.CharField(max_length=200, required=False, allow_blank=True)

    class Meta:
        model = Action
        fields = (
            'agenda_id',
            'action_id',
            'action_title',
            'person',
            'dead_line',
        )

    def create(self, validated_data):
        agenda_id = Agenda.objects.get(agenda_id=validated_data['agenda_id'])
        action_title = ""
        person = ""
        if "action_title" in validated_data:
            action_title = validated_data['action_title']
        if "person" in validated_data:
            person = validated_data['person']

        action = Action.objects.create(
            agenda_id=agenda_id,
            action_title=action_title,
            person=person
        )
        return action


class SelfCheckSerializer(serializers.ModelSerializer):
    meet_id = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = SelfCheck
        fields = (
            'meet_id',
            'check_id',
            'check1',
            'check2',
            'check3',
            'check4',
            'check5',
            'check6',
            'check7',
            'check8',
            'check9',
            'check10',
        )

    def create(self, validated_data):
        meet_id = Meet.objects.get(meet_id=validated_data['meet_id'])
        check1 = ""
        check2 = ""
        check3 = ""
        check4 = ""
        check5 = ""
        check6 = ""
        check7 = ""
        check8 = ""
        check9 = ""
        check10 = ""
        if "check1" in validated_data:
            check1 = validated_data['check1']
        if "check2" in validated_data:
            check2 = validated_data['check2']
        if "check3" in validated_data:
            check3 = validated_data['check3']
        if "check4" in validated_data:
            check4 = validated_data['check4']
        if "check5" in validated_data:
            check5 = validated_data['check5']
        if "check6" in validated_data:
            check6 = validated_data['check6']
        if "check7" in validated_data:
            check7 = validated_data['check7']
        if "check8" in validated_data:
            check8 = validated_data['check8']
        if "check9" in validated_data:
            check9 = validated_data['check9']
        if "check10" in validated_data:
            check10 = validated_data['check10']
        selfcheck = SelfCheck.objects.create(
            meet_id=meet_id,
            check1=check1,
            check2=check2,
            check3=check3,
            check4=check4,
            check5=check5,
            check6=check6,
            check7=check7,
            check8=check8,
            check9=check9,
            check10=check10,
        )
        return selfcheck


class SecessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secession
        fields = (
            'email',
            'cause',
            'reg_date',
        )


# 유저 db저장
class UsersaveSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(max_length=200, default="")
    img = serializers.CharField(max_length=500, default="")

    class Meta:
        model = User
        fields = ['password', 'email', 'name', 'img', 'provider', 'nickname']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            provider=validated_data['provider'],
            img=validated_data['img'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserchkSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    nickname = serializers.CharField(max_length=200, allow_null=True, required=False)
    secession_chk = serializers.CharField(max_length=200, allow_null=True, required=False)

    def validate(self, data):
        email = data.get('email')
        if data.get('nickname'):
            nickname = data.get('nickname')
        else:
            nickname = 'None'

        try:
            user = User_auth.objects.get(email=email)
        except User_auth.DoesNotExist:
            user = 'None'

        if user == 'None':
            try:
                secession_email = Secession.objects.filter(email=email).order_by('-reg_date')[0:1]
                if secession_email[0].reg_date:
                    start_date = secession_email[0].reg_date
                    end_date = start_date + timedelta(days=1)

                    var = Secession.objects.filter(
                        Q(email=email) and Q(reg_date__range=[start_date, end_date])).order_by('-reg_date')[0:1]

                    if var:
                        secession_chk = 'True'
                    else:
                        secession_chk = 'None'
                else:
                    secession_chk = 'None'

            except:
                secession_chk = 'None'
        else:
            secession_chk = 'None'

        return {'email': user, 'nickname': nickname, 'secession_chk': secession_chk}


# 유저 로그인 진행
User_auth = get_user_model()

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER


class UserloginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200, required=False)
    password = serializers.CharField(max_length=200, write_only=True, required=False)
    name = serializers.CharField(max_length=200, required=False)
    nickname = serializers.CharField(max_length=200, required=False)
    token = serializers.CharField(max_length=255, read_only=True, required=False)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        name = data.get('name', None)
        nickname = data.get('nickname', None)

        try:
            user = User.objects.get(email=email, name=name, nickname=nickname)

            if user.check_password(password):
                payload = JWT_PAYLOAD_HANDLER(user)
                token = JWT_ENCODE_HANDLER(payload)

                update_last_login(None, user)
            else:
                return {'token': "user_info errors"}
        except:
            return {'token': "user_info errors"}

        return {'token': token}

