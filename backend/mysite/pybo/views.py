# backend/post/views.py
import json
from typing import Dict

from django.http import HttpResponse
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
            user_id = User.objects.get(id=token['user_id'])
            self.request = user_id.id
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
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    #post(회원가입, 로그인)
    @permission_classes([AllowAny])
    def create(self, request, *args, **kwargs):
        print(request.data[0])
        if not'email' in request.data[0] or not'password' in request.data[0] or not'name' in request.data[0]:
            response_messages = {
                'success': False,
                'messages': 'data_fild errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

        serializer = UserchkSerializer(data=request.data, many=True)
        serializer.is_valid()
        email = serializer.data[0]['email']
        nickname = serializer.data[0]['nickname']
        secession_chk = serializer.data[0]['secession_chk']
        if secession_chk == 'True':
            response_messages = {
                'messages': 'secession period'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

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
            user_info = User.objects.get(id=user_id)

            if request.method == 'PUT' or request.method == 'PATCH':
                if 'email' in request.data or 'password' in request.data:
                    response_messages = {
                        'success': False,
                        'messages': 'data_fild errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)
                try:
                    serializer = UserSerializer(instance=user_info, data=request.data)
                    serializer.is_valid()
                    serializer.save()

                    user_info = serializer.data
                    user_info.pop('password')

                    return Response(user_info, status=status.HTTP_200_OK)
                except:
                    response_messages = {
                        'success': False,
                        'messages': 'user_update errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                cause = ''
                if request.data:
                    if 'cause' in request.data:
                        cause = request.data['cause']

                try:
                    delete = Secession()
                    delete.email = user_info.email
                    delete.cause = cause
                    delete.save()

                    user_info.delete()

                    response_messages = {
                        'success': True
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)

                except:
                    response_messages = {
                        'success': False
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)

            else:
                response_messages = {
                    'success': False,
                    'messages': 'user_delete errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

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

    #get
    def list(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            meet_where = Q(user_id=user_id)
            if request.GET:
                if 'meet_id' in request.GET:
                    meet_where.add(Q(meet_id=request.GET['meet_id']), meet_where.AND)

                if 'meet_status' in request.GET:
                    meet_where.add(Q(meet_status=request.GET['meet_status']), meet_where.AND)

                if 'rm_status' in request.GET:
                    meet_where.add(Q(rm_status=request.GET['rm_status']), meet_where.AND)

            try:
                meet_info = Meet.objects.filter(meet_where)
                serializer = MeetSerializer(meet_info, many=True)
                meet_info_list = serializer.data
                return Response(meet_info_list, status=status.HTTP_200_OK)
            except:
                response_messages = {
                    'success': False,
                    'messages': 'meet_info errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

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
                response_messages = {
                    'success': False,
                    'messages': 'meet_save errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)
        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

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

                    serializer = MeetSerializer(instance=meet_info, data=meet_info_json)
                    serializer.is_valid()
                    serializer.save()

                    meet_info = serializer.data

                    return Response(meet_info, status=status.HTTP_200_OK)
                except:
                    response_messages = {
                        'success': False,
                        'messages': 'meet_update errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                if request.data:
                    if not'meet_id' in request.data:
                        response_messages = {
                            'success': False,
                            'messages': 'data_fild errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)
                    try:
                        response_messages = {
                            'success': True,
                            'meet': 'delete ok'
                        }

                        meet_id = request.data['meet_id']
                        meet_info = Meet.objects.get(user_id=user_id, meet_id=meet_id)
                        agenda_info = Agenda.objects.filter(meet_id=meet_info.meet_id)
                        action_info = Action.objects.select_related('agenda_id').filter(agenda_id__meet_id=meet_info.meet_id)

                        if agenda_info:
                            agenda_info.delete()
                            response_messages.update({'agenda': 'delete ok'})

                        if action_info:
                            action_info.delete()
                            response_messages.update({'action': 'delete ok'})

                        meet_info.delete()

                        return Response(response_messages, status=status.HTTP_200_OK)
                    except:
                        response_messages = {
                            'success': False,
                            'messages': 'meet_delete errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)
                else:
                    meet_info = Meet.objects.filter(user_id=user_id)
                    if meet_info:
                        response_messages = {
                            'success': True,
                            'meet_all': 'delete ok'
                        }

                        agenda_info = Agenda.objects.select_related('meet_id').filter(meet_id__user_id=user_id)
                        action_info = Action.objects.select_related('agenda_id', 'agenda_id__meet_id').filter(agenda_id__meet_id__user_id=user_id)

                        if agenda_info:
                            response_messages.update({'agenda_all': 'delete ok'})

                        if action_info:
                            response_messages.update({'action_all': 'delete ok'})

                        action_info.delete()
                        agenda_info.delete()
                        meet_info.delete()

                        return Response(response_messages, status=status.HTTP_200_OK)
                    else:
                        response_messages = {
                            'success': False,
                            'messages': 'meet_data None'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)
            else:
                response_messages = {
                    'success': False,
                    'messages': 'method errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            meet_info = Meet.objects.filter(user_id=user_id, meet_id=kwargs['pk'])

            if meet_info:
                serializer = MeetSerializer(data=meet_info, many=True)
                serializer.is_valid()

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response_messages = {
                    'success': False,
                    'messages': 'meet_info errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                meet_info = Meet.objects.get(user_id=user_id, meet_id=kwargs['pk'])
                data = request.data
                data.update({'user_id': user_id})
                serializer = MeetSerializer(instance=meet_info, data=data)
                serializer.is_valid()
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                response_messages = {
                    'success': False,
                    'messages': 'meet_update errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                meet_info = Meet.objects.get(user_id=user_id, meet_id=kwargs['pk'])

                response_messages = {
                    'success': True,
                    'meet': 'delete ok'
                }

                agenda_info = Agenda.objects.filter(meet_id=meet_info.meet_id)
                action_info = Action.objects.select_related('agenda_id').filter(agenda_id__meet_id=meet_info.meet_id)

                if agenda_info:
                    response_messages.update({'agenda_all': 'delete ok'})

                if action_info:
                    response_messages.update({'action_all': 'delete ok'})

                action_info.delete()
                agenda_info.delete()
                meet_info.delete()

                return Response(response_messages, status=status.HTTP_200_OK)
            except:
                response_messages = {
                    'success': False,
                    'messages': 'meet_delete errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def list(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            agenda_where = Q()
            if request.GET:
                if 'meet_id' in request.GET:
                    agenda_where.add(Q(meet_id=request.GET['meet_id']), agenda_where.AND)

                if 'agenda_id' in request.GET:
                    agenda_where.add(Q(agenda_id=request.GET['agenda_id']), agenda_where.AND)

                if 'agenda_status' in request.GET:
                    agenda_where.add(Q(agenda_status=request.GET['agenda_status']), agenda_where.AND)
            try:
                agenda_info = Agenda.objects.filter(agenda_where).select_related('meet_id').filter(meet_id__user_id=user_id).order_by('order_number')
                serializer = AgendaSerializer(data=agenda_info, many=True)
                serializer.is_valid()

                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                response_messages = {
                    'success': False,
                    'messages': 'agenda_info errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            if isinstance(request.data, list):
                response_array = []
                for i in request.data:
                    if not'meet_id' in i or not'setting_time' in i or not'order_number' in i:
                        response_messages = {
                            'success': False,
                            'messages': 'data_fild errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)
                    try:
                        Meet.objects.get(user_id=user_id, meet_id=i['meet_id']) #유저의 meet_id인지 체크

                        serializer = AgendaSerializer(data=i)
                        serializer.is_valid()
                        serializer.save()

                        agenda_info = serializer.data
                        progress_json = [{
                            "agenda_id": agenda_info['agenda_id'],
                            "progress_time": agenda_info['progress_time']
                        }]

                        progress_serializer = ProgressSerializer(data=progress_json, many=True)
                        progress_serializer.is_valid()
                        progress_serializer.save()

                        response_array.append(serializer.data)
                        response_array.append(progress_serializer.data[0])
                    except:
                        response_messages = {
                            'success': False,
                            'messages': 'agenda_array_save errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)

                return Response(response_array, status=status.HTTP_200_OK)

            else:
                if not'meet_id' in request.data or not'setting_time' in request.data or not'order_number' in request.data:
                    response_messages = {
                        'success': False,
                        'messages': 'data_fild errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)
                try:
                    Meet.objects.get(user_id=user_id, meet_id=request.data['meet_id'])  # 유저의 meet_id인지 체크

                    serializer = AgendaSerializer(data=request.data)
                    serializer.is_valid()
                    serializer.save()
                    agenda_info = serializer.data

                    progress_json = [{
                        "agenda_id": agenda_info['agenda_id'],
                        "progress_time": agenda_info['progress_time']
                    }]

                    progress_serializer = ProgressSerializer(data=progress_json, many=True)
                    progress_serializer.is_valid()
                    progress_serializer.save()

                    agenda_info.update(progress_serializer.data[0])
                except:
                    response_messages = {
                        'success': False,
                        'messages': 'agenda_save errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)

                return Response(agenda_info, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            if request.method == 'PUT' or request.method == 'PATCH':
                if isinstance(request.data, list):
                    response_array = []
                    for i in request.data:
                        try:
                            meet_id = Meet.objects.get(user_id=user_id, meet_id=i['meet_id']) # 유저의 meet_id인지 체크

                            agenda_info = Agenda.objects.select_related('meet_id').filter(meet_id__user_id=user_id).get(agenda_id=i['agenda_id'], meet_id=meet_id.meet_id)
                            serializer = AgendaSerializer(instance=agenda_info, data=i)
                            serializer.is_valid()
                            serializer.save()
                            response_array.append(serializer.data)
                        except:
                            response_messages = {
                                'success': False,
                                'messages': 'agenda_array_update errors'
                            }
                            return Response(response_messages, status=status.HTTP_200_OK)

                    return Response(response_array, status=status.HTTP_200_OK)

                else:
                    try:
                        meet_id = Meet.objects.get(user_id=user_id, meet_id=request.data['meet_id'])  # 유저의 meet_id인지 체크

                        agenda_info = Agenda.objects.select_related('meet_id').filter(meet_id__user_id=user_id).get(agenda_id=request.data['agenda_id'], meet_id=meet_id.meet_id)
                        serializer = AgendaSerializer(instance=agenda_info, data=request.data)
                        serializer.is_valid()
                        serializer.save()

                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except:
                        response_messages = {
                            'success': False,
                            'messages': 'agenda_update errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                if isinstance(request.data, list):
                    response_messages = {
                        'success': True,
                        'agenda': 'delete ok'
                    }
                    for i in request.data:
                        try:

                            meet_id = Meet.objects.get(user_id=user_id, meet_id=i['meet_id'])  # 유저의 meet_id인지 체크

                            if not'agenda_id' in i:
                                response_messages = {
                                    'success': False,
                                    'messages': 'agenda_delete_key errors'
                                }
                                return Response(response_messages, status=status.HTTP_200_OK)

                            agenda_info = Agenda.objects.select_related('meet_id').filter(meet_id__user_id=user_id).get(agenda_id=i['agenda_id'], meet_id=meet_id.meet_id)
                            action_info = Action.objects.select_related('agenda_id').filter(agenda_id__meet_id=meet_id.meet_id)

                            if action_info:
                                action_info.delete()
                                response_messages.update({'action': 'delete ok'})
                            agenda_info.delete()
                        except:
                            response_messages = {
                                'success': False,
                                'messages': 'agenda_array_delete errors'
                            }
                            return Response(response_messages, status=status.HTTP_200_OK)

                    return Response(response_messages, status=status.HTTP_200_OK)

                else:
                    try:
                        response_messages = {
                            'success': True,
                            'agenda': 'delete ok'
                        }

                        meet_id = Meet.objects.get(user_id=user_id, meet_id=request.data['meet_id'])  # 유저의 meet_id인지 체크

                        agenda_info = Agenda.objects.select_related('meet_id').filter(meet_id__user_id=user_id).get(agenda_id=request.data['agenda_id'])
                        action_info = Action.objects.select_related('agenda_id').filter(agenda_id__meet_id=meet_id.meet_id)
                        if action_info:
                            action_info.delete()
                            response_messages.update({'action': 'delete ok'})

                        agenda_info.delete()

                        return Response(response_messages, status=status.HTTP_200_OK)

                    except:
                        response_messages = {
                            'success': False,
                            'messages': 'agenda_delete errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)

            else:
                response_messages = {
                    'success': False,
                    'messages': 'method errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)
        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                agenda_info = Agenda.objects.filter(agenda_id=kwargs['pk']).select_related('meet_id')\
                    .filter(meet_id__user_id=user_id)

                serializer = AgendaSerializer(data=agenda_info, many=True)
                serializer.is_valid()

                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                response_messages = {
                    'success': False,
                    'messages': 'agenda_info errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)
        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            try:
                agenda_info = Agenda.objects.select_related('meet_id') \
                    .filter(meet_id__user_id=user_id).get(agenda_id=kwargs['pk'])
                agenda_json = {'meet_id': agenda_info.meet_id.meet_id}
                agenda_json.update(request.data)

                serializer = AgendaSerializer(instance=agenda_info, data=agenda_json)
                serializer.is_valid()
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                response_messages = {
                    'success': False,
                    'messages': 'agenda_update errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)
        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                response_messages = {
                    'success': True,
                    'agenda': 'delete ok'
                }

                agenda_info = Agenda.objects.select_related('meet_id').filter(meet_id__user_id=user_id).get(agenda_id=kwargs['pk'])
                action_info = Action.objects.filter(agenda_id=agenda_info.agenda_id)

                if action_info:
                    action_info.delete()
                    response_messages.update({'action': 'delete ok'})

                agenda_info.delete()

                return Response(response_messages, status=status.HTTP_200_OK)
            except:
                response_messages = {
                    'success': False,
                    'messages': 'agenda_delete errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Agenda_progress.objects.all()
    serializer_class = ProgressSerializer


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def list(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            action_where = Q()
            if request.GET:
                if 'agenda_id' in request.GET:
                    action_where.add(Q(agenda_id=request.GET['agenda_id']), action_where.AND)

                if 'action_id' in request.GET:
                    action_where.add(Q(action_id=request.GET['action_id']), action_where.AND)

            try:
                action_info = Action.objects.filter(action_where).select_related('agenda_id', 'agenda_id__meet_id').filter(agenda_id__meet_id__user_id=user_id)

                serializer = ActionSerializer(data=action_info, many=True)
                serializer.is_valid()
                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                response_messages = {
                    'success': False,
                    'messages': 'action_info errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            if isinstance(request.data, list):
                response_array = []
                for i in request.data:
                    if not"agenda_id" in i:
                        response_messages = {
                            'success': False,
                            'messages': 'data_fild errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)

                    try:
                        # 해당 유저의 agenda_id 맞는지 체크
                        Action.objects.filter(agenda_id=i['agenda_id']).select_related('agenda_id', 'agenda_id__meet_id').filter(agenda_id__meet_id__user_id=user_id)

                        serializer = ActionSerializer(data=i)
                        serializer.is_valid()
                        serializer.save()

                        response_array.append(serializer.data)

                    except:
                        response_messages = {
                            'success': False,
                            'messages': 'action_array_save errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)

                return Response(response_array, status=status.HTTP_200_OK)

            else:
                if not"agenda_id" in request.data:
                    response_messages = {
                        'success': False,
                        'messages': 'data_fild errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)
                try:
                    # 해당 유저의 agenda_id 맞는지 체크
                    Action.objects.filter(agenda_id=request.data['agenda_id']).select_related('agenda_id', 'agenda_id__meet_id').filter(agenda_id__meet_id__user_id=user_id)

                    serializer = ActionSerializer(data=request.data)
                    serializer.is_valid()
                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)

                except:
                    response_messages = {
                        'success': False,
                        'messages': 'action_save errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)
        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            if request.method == 'PUT' or request.method == 'PATCH':
                if isinstance(request.data, list):
                    response_array = []
                    for i in request.data:
                        try:
                            # 해당 유저의 agenda_id 맞는지 체크
                            action_info = Action.objects.select_related('agenda_id', 'agenda_id__meet_id')\
                                .filter(agenda_id__meet_id__user_id=user_id).get(action_id=i['action_id'])

                            serializer = ActionSerializer(instance=action_info, data=i)
                            serializer.is_valid()
                            serializer.save()

                            response_array.append(serializer.data)
                        except:
                            response_messages = {
                                'success': False,
                                'messages': 'action_array_update errors'
                            }
                            return Response(response_messages, status=status.HTTP_200_OK)

                    return Response(response_array, status=status.HTTP_200_OK)
                else:
                    try:
                        # 해당 유저의 agenda_id 맞는지 체크
                        action_info = Action.objects.select_related('agenda_id', 'agenda_id__meet_id') \
                            .filter(agenda_id__meet_id__user_id=user_id).get(action_id=request.data['action_id'])

                        serializer = ActionSerializer(instance=action_info, data=request.data)
                        serializer.is_valid()
                        serializer.save()

                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except:
                        response_messages = {
                            'success': False,
                            'messages': 'action_update errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)

            elif request.method == 'DELETE':
                if isinstance(request.data, list):
                    for i in request.data:
                        try:
                            # 해당 유저의 agenda_id 맞는지 체크
                            action_info = Action.objects.select_related('agenda_id', 'agenda_id__meet_id') \
                                .filter(agenda_id__meet_id__user_id=user_id).get(agenda_id=i['agenda_id'], action_id=i['action_id'])

                            action_info.delete()

                        except:
                            response_messages = {
                                'success': False,
                                'messages': 'action_array_delete errors'
                            }
                            return Response(response_messages, status=status.HTTP_200_OK)

                    response_messages = {
                        'success': True,
                        'action': 'delete ok'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)

                else:
                    try:

                        if not'action_id' in request.data:
                            response_messages = {
                                'success': False,
                                'messages': 'data_fild errors'
                            }
                            return Response(response_messages, status=status.HTTP_200_OK)

                        # 해당 유저의 agenda_id 맞는지 체크
                        action_info = Action.objects.select_related('agenda_id', 'agenda_id__meet_id').filter(agenda_id__meet_id__user_id=user_id).get(action_id=request.data['action_id'])

                        action_info.delete()

                        response_messages = {
                            'success': True,
                            'action': 'delete ok'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)
                    except:
                        response_messages = {
                            'success': False,
                            'messages': 'action_delete errors'
                        }
                        return Response(response_messages, status=status.HTTP_200_OK)

            else:
                response_messages = {
                    'success': False,
                    'messages': 'method errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            action_info = Action.objects.filter(action_id=kwargs['pk']).select_related('agenda_id', 'agenda_id__meet_id').filter(
                agenda_id__meet_id__user_id=user_id)

            if action_info:
                serializer = ActionSerializer(data=action_info, many=True)
                serializer.is_valid()

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response_messages = {
                    'success': False,
                    'messages': 'action_info errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                action_info = Action.objects.select_related('agenda_id', 'agenda_id__meet_id').filter(
                    agenda_id__meet_id__user_id=user_id).get(action_id=kwargs['pk'])

                serializer = ActionSerializer(instance=action_info, data=request.data)
                serializer.is_valid()
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                response_messages = {
                    'success': False,
                    'messages': 'action_update errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                action_info = Action.objects.select_related('agenda_id', 'agenda_id__meet_id').filter(
                    agenda_id__meet_id__user_id=user_id).get(action_id=kwargs['pk'])

                action_info.delete()

                response_messages = {
                    'success': True,
                    'action': 'delete ok'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

            except:
                response_messages = {
                    'success': False,
                    'messages': 'action_delete errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)


class SelfCheckViewSet(viewsets.ModelViewSet):
    queryset = SelfCheck.objects.all()
    serializer_class = SelfCheckSerializer

    def list(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()
            selfcheck_where = Q()

            if request.GET:
                if 'meet_id' in request.GET:
                    selfcheck_where.add(Q(meet_id=request.GET['meet_id']), selfcheck_where.AND)

                if 'check_id' in request.GET:
                    selfcheck_where.add(Q(check_id=request.GET['check_id']), selfcheck_where.AND)
            try:

                selfcheck_info = SelfCheck.objects.filter(selfcheck_where).select_related('meet_id').filter(meet_id__user_id=user_id)

                serializer = SelfCheckSerializer(data=selfcheck_info, many=True)
                serializer.is_valid()

                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                response_messages = {
                    'success': False,
                    'messages': 'selfcheck_info errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                Meet.objects.get(meet_id=request.data['meet_id'], user_id=user_id) # 해당 유저의 meet_id가 맞는지

                serializer = SelfCheckSerializer(data=request.data)
                serializer.is_valid()
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                response_messages = {
                    'success': False,
                    'messages': 'selfcheck_save errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            if request.method == 'PUT' or request.method == 'PATCH':
                try:
                    selfcheck_info = SelfCheck.objects.select_related('meet_id').filter(meet_id__user_id=user_id).get(
                        check_id=request.data['check_id'])

                    serializer = SelfCheckSerializer(instance=selfcheck_info, data=request.data)
                    serializer.is_valid()
                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    response_messages = {
                        'success': False,
                        'messages': 'selfcheck_save errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)

            if request.method == 'DELETE':
                try:
                    selfcheck_info = SelfCheck.objects.select_related('meet_id').filter(meet_id__user_id=user_id).get(
                        check_id=request.data['check_id'])

                    selfcheck_info.delete()

                    response_messages = {
                        'success': True,
                        'action': 'delete ok'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)
                except:
                    response_messages = {
                        'success': True,
                        'messages': 'selfcheck_delete errors'
                    }
                    return Response(response_messages, status=status.HTTP_200_OK)

            else:
                response_messages = {
                    'success': False,
                    'messages': 'method errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            selfcheck_info = SelfCheck.objects.filter(check_id=kwargs['pk']).select_related('meet_id').filter(
                meet_id__user_id=user_id)

            if selfcheck_info:
                serializer = SelfCheckSerializer(data=selfcheck_info, many=True)
                serializer.is_valid()

                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                response_messages = {
                    'success': False,
                    'messages': 'SelfCheck_info errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                selfcheck_info = SelfCheck.objects.select_related('meet_id').filter(
                    meet_id__user_id=user_id).get(check_id=kwargs['pk'])

                serializer = SelfCheckSerializer(instance=selfcheck_info, data=request.data)
                serializer.is_valid()
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                response_messages = {
                    'success': False,
                    'messages': 'selfcheck_update errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if TokenChk(request).chk() != 'None':
            user_id = TokenChk(request).chk()

            try:
                selfcheck_info = SelfCheck.objects.select_related('meet_id').filter(
                    meet_id__user_id=user_id).get(check_id=kwargs['pk'])

                selfcheck_info.delete()

                response_messages = {
                    'success': True,
                    'selfcheck': 'delete ok'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

            except:
                response_messages = {
                    'success': False,
                    'messages': 'selfcheck_delete errors'
                }
                return Response(response_messages, status=status.HTTP_200_OK)

        else:
            response_messages = {
                'success': False,
                'messages': 'token errors'
            }
            return Response(response_messages, status=status.HTTP_200_OK)



