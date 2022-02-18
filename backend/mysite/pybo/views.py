#backend/post/views.py
from django.shortcuts import render
from django.views import View
from rest_framework import generics, viewsets, status, filters
# from django_filters import rest_framework as filters
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MeetViewSet(viewsets.ModelViewSet):
    queryset = Meet.objects.all()
    serializer_class = MeetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['rm_status', 'meet_status']


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


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserchkSerializer(data=request.data, many=True)
    serializer.is_valid()
    if serializer.data[0]['email'] == 'None':
        serializer = UsersaveSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    serializer = UserloginSerializer(data=request.data, many=True)
    serializer.is_valid()
    token = serializer.validated_data[0]['token']
    res = {'success': True}
    response = Response(res, status=status.HTTP_200_OK)
    response.set_cookie("token", token, 7)
    return response


