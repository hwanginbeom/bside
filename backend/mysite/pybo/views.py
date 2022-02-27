# backend/post/views.py
import json
from typing import Dict

from django.shortcuts import render
from django.views import View
from rest_framework import generics, viewsets, status, filters, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import *
from .serializers import *

JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER


#토큰 체크
class TokenChk:
    def __init__(self, request):
        try:
            header_token = request.META['HTTP_AUTHORIZATION']
            token = JWT_DECODE_HANDLER(header_token)
            self.request = token['user_id']
        except:
            self.request = 'None'

    def chk(self):
        return self.request


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #get
    def list(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            user_info = User.objects.get(id=user_id)
            user_info = {
                'id': user_info.id,
                'email': user_info.email,
                'name': user_info.name,
                'nickname': user_info.nickname,
                'img': user_info.img,
                'last_login': user_info.last_login,
                'join_date': user_info.join_date,
                'provider': user_info.provider,
            }

            return Response(user_info, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_200_OK)

    #post(회원가입, 로그인)
    @permission_classes([AllowAny])
    def create(self, request, *args, **kwargs):
        serializer = UserchkSerializer(data=request.data, many=True)
        serializer.is_valid()
        email = serializer.data[0]['email']
        nickname = serializer.data[0]['nickname']
        secession_chk = serializer.data[0]['secession_chk']
        if secession_chk == 'True':
            res = {'success': 'False'}
            return Response(res, status=status.HTTP_200_OK)

        if email == 'None':  # db 유저 데이터 없을때
            if nickname == 'None':  # 닉네임 데이터 안넘어 왔을때 db입력x
                res = {'db': 'None'}
                return Response(res, status=status.HTTP_200_OK)
            else:  # 닉네임 데이터 넘어왔을때 db입력o
                serializer = UsersaveSerializer(data=request.data, many=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                # db 저장후 토큰발급
                serializer = UserloginSerializer(data=request.data, many=True)
                serializer.is_valid()
                token = serializer.validated_data[0]['token']
                res = {'success': True, 'token': token}
                response = Response(res, status=status.HTTP_200_OK)
                return response
        else:  # db 유저 데이터 있을때 바로 token 발급
            serializer = UserloginSerializer(data=request.data, many=True)
            serializer.is_valid()
            token = serializer.validated_data[0]['token']
            res = {'success': True, 'token': token}
            response = Response(res, status=status.HTTP_200_OK)
            return response

    #update, delete
    def http_method_not_allowed(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            #user 정보 체크
            try:
                user_info = User.objects.get(id=user_id)
            except:
                return Response({'success': False}, status=status.HTTP_200_OK)

            if request.method == 'PUT' or request.method == 'PATCH':
                try:
                    serializer = UserSerializer(instance=user_info, data=request.data)
                    serializer.is_valid()
                    serializer.save()
                    user_info = serializer.data
                    return Response(user_info, status=status.HTTP_200_OK)
                except:
                    return Response({'success': False}, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                user_info.delete()
                user_info = {'success': True}
                return Response(user_info, status=status.HTTP_200_OK)

            else:
                return Response({'success': False}, status=status.HTTP_200_OK)

        else:
            return Response({'success': False}, status=status.HTTP_200_OK)

    # --- 키값요청 메서드 종료처리
    def update(self, request, *args, **kwargs):
        return Response({'success': False}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response({'success': False}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response({'success': False}, status=status.HTTP_200_OK)
    # ---


class MeetViewSet(viewsets.ModelViewSet):
    queryset = Meet.objects.all()
    serializer_class = MeetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['rm_status', 'meet_status']

    #get
    def list(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            if request.data:
                if 'meet_id' in request.data and not'meet_status' in request.data and not'rm_status' in request.data: #meet_id(o), meet_status(x), rm_status(x)
                    meet_id = request.data['meet_id']
                    try:
                        meet_info = Meet.objects.filter(user_id=user_id, meet_id=meet_id)
                        serializer = MeetSerializer(meet_info, many=True)
                        meet_info_list = serializer.data
                        return Response(meet_info_list, status=status.HTTP_200_OK)
                    except:
                        return Response({'success': False}, status=status.HTTP_200_OK)

                elif 'meet_id' in request.data and 'meet_status' in request.data and not'rm_status' in request.data: #meet_id(o), meet_status(o), rm_status(x)
                    meet_id = request.data['meet_id']
                    meet_status = request.data['meet_status']
                    try:
                        meet_info = Meet.objects.filter(user_id=user_id, meet_id=meet_id, meet_status=meet_status)
                        serializer = MeetSerializer(meet_info, many=True)
                        meet_info_list = serializer.data
                        return Response(meet_info_list, status=status.HTTP_200_OK)
                    except:
                        return Response({'success': False}, status=status.HTTP_200_OK)

                elif 'meet_id' in request.data and 'meet_status' in request.data and 'rm_status' in request.data: #meet_id(o), meet_status(o), rm_status(o)
                    meet_id = request.data['meet_id']
                    meet_status = request.data['meet_status']
                    rm_status = request.data['rm_status']
                    try:
                        meet_info = Meet.objects.filter(user_id=user_id, meet_id=meet_id, meet_status=meet_status,
                                                        rm_status=rm_status)
                        serializer = MeetSerializer(meet_info, many=True)
                        meet_info_list = serializer.data
                        return Response(meet_info_list, status=status.HTTP_200_OK)
                    except:
                        return Response({'success': False}, status=status.HTTP_200_OK)

                elif not'meet_id' in request.data and 'meet_status' in request.data and 'rm_status' in request.data: #meet_id(x), meet_status(o), rm_status(o)
                    meet_status = request.data['meet_status']
                    rm_status = request.data['rm_status']
                    try:
                        meet_info = Meet.objects.filter(user_id=user_id, meet_status=meet_status, rm_status=rm_status)
                        serializer = MeetSerializer(meet_info, many=True)
                        meet_info_list = serializer.data
                        return Response(meet_info_list, status=status.HTTP_200_OK)
                    except:
                        return Response({'success': False}, status=status.HTTP_200_OK)

                elif not'meet_id' in request.data and 'meet_status' in request.data and not'rm_status' in request.data:  # meet_id(x), meet_status(o), rm_status(x)
                    meet_status = request.data['meet_status']
                    try:
                        meet_info = Meet.objects.filter(user_id=user_id, meet_status=meet_status)
                        serializer = MeetSerializer(meet_info, many=True)
                        meet_info_list = serializer.data
                        return Response(meet_info_list, status=status.HTTP_200_OK)
                    except:
                        return Response({'success': False}, status=status.HTTP_200_OK)

                elif not'meet_id' in request.data and not'meet_status' in request.data and 'rm_status' in request.data:  # meet_id(x), meet_status(x), rm_status(o)
                    rm_status = request.data['rm_status']
                    try:
                        meet_info = Meet.objects.filter(user_id=user_id, rm_status=rm_status)
                        serializer = MeetSerializer(meet_info, many=True)
                        meet_info_list = serializer.data
                        return Response(meet_info_list, status=status.HTTP_200_OK)
                    except:
                        return Response({'success': False}, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False}, status=status.HTTP_200_OK)
            else:
                try:
                    meet_info = Meet.objects.filter(user_id=user_id)
                    serializer = MeetSerializer(meet_info, many=True)
                    meet_info_list = serializer.data
                    return Response(meet_info_list, status=status.HTTP_200_OK)
                except:
                    return Response({'success': False}, status=status.HTTP_200_OK)

        else:
            return Response({'success': False}, status=status.HTTP_200_OK)

    #post
    def create(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            try:
                meet_info = {
                    "user_id": user_id,
                    "meet_title": request.data['meet_title'],
                    "meet_date": datetime.strptime(request.data['meet_date'], "%Y-%m-%d %H:%M:%S"),
                    "meet_status": request.data['meet_status'],
                    "rm_status": request.data['rm_status'],
                    "participants": request.data['participants'],
                    'goal': request.data['goal'],
                }
                serializer = MeetSerializer(data=meet_info)
                serializer.is_valid()
                serializer.save()
                meet_save_info = serializer.data
                return Response(meet_save_info, status=status.HTTP_200_OK)
            except:
                return Response({'success': False}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_200_OK)

    #update, delete
    def http_method_not_allowed(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            if request.method == 'PUT' or request.method == 'PATCH':
                try:
                    meet_id = request.data['meet_id']
                    meet_info = Meet.objects.get(user_id=user_id, meet_id=meet_id)
                    # json 합치기
                    meet_info_json = {'user_id': user_id}
                    meet_info_json.update(request.data)
                except:
                    return Response({'success': False}, status=status.HTTP_200_OK)

                serializer = MeetSerializer(instance=meet_info, data=meet_info_json)
                serializer.is_valid()
                serializer.save()

                meet_info = serializer.data

                return Response(meet_info, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                if request.data:
                    meet_id = request.data['meet_id']
                    meet_info = Meet.objects.get(user_id=user_id, meet_id=meet_id)
                    meet_info.delete()
                    return Response({'success': True}, status=status.HTTP_200_OK)
                else:
                    meet_info = Meet.objects.filter(user_id=user_id)
                    meet_info.delete()
                    return Response({'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False}, status=status.HTTP_200_OK)

        else:
            return Response({'success': False}, status=status.HTTP_200_OK)

    # --- 키값요청 메서드 종료처리
    def update(self, request, *args, **kwargs):
        return Response({'success': False}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response({'success': False}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response({'success': False}, status=status.HTTP_200_OK)
    # ---


class MeetsList(generics.ListAPIView):
    serializer_class = MeetSerializer
    print('됨?')

    def get_queryset(self):
        if self.kwargs['meet_status'] is not None:
            meet_status = self.kwargs['meet_status']
            return Meet.objects.filter(meet_status=meet_status[-1]).order_by('meet_id')
        elif self.kwargs['rm_status'] is not None:
            rm_status = self.kwargs['rm_status']
            return Meet.objects.filter(rm_status=rm_status[-1]).order_by('meet_id')


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    # def list(self, request, *args, **kwargs):



class AgendasList(generics.ListAPIView):
    serializer_class = AgendaSerializer

    def get_queryset(self):
        meet_id = self.kwargs['meet_id']
        return Agenda.objects.filter(meet_id=meet_id).order_by('order_number')


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ActionsList(generics.ListAPIView):
    serializer_class = ActionSerializer

    def get_queryset(self):
        agenda_id = self.kwargs['agenda_id']
        return Action.objects.filter(agenda_id=agenda_id)


class SelfCheckViewSet(viewsets.ModelViewSet):
    queryset = SelfCheck.objects.all()
    serializer_class = SelfCheckSerializer


class SelfChecksList(generics.ListAPIView):
    serializer_class = SelfCheckSerializer

    def get_queryset(self):
        meet_id = self.kwargs['meet_id']
        return SelfCheck.objects.filter(meet_id=meet_id)


class SecessionSerializer(viewsets.ModelViewSet):
    queryset = Secession.objects.all()
    serializer_class = SecessionSerializer

