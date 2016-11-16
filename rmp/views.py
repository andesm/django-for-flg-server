# coding=utf-8
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from rmp.models import Rmp
from rmp.permissions import IsOwnerOrReadOnly
from rmp.serializers import UserSerializer, RmpSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RmpViewSet(viewsets.ModelViewSet):
    serializer_class = RmpSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        rmp = Rmp.objects.filter(file=serializer.initial_data['id']).first()
        if rmp is None:
            serializer.save(owner=self.request.user)
        else:
            raise ValidationError('Rmp file exists! %s %d %d %d'
                                  % (rmp.file, rmp.id, rmp.count, rmp.skip))

    def perform_update(self, serializer):
        rmp = Rmp.objects.get(id=serializer.initial_data['id'])
        if serializer.validated_data['file'] == rmp.file and \
                (rmp.count <= serializer.initial_data['count'] or rmp.skip <= serializer.initial_data['skip']):
            serializer.save()
        else:
            raise ValidationError('Mismatch ID? %s %d %d %d'
                                  % (rmp.file, rmp.id, rmp.count, rmp.skip))

    def get_queryset(self):
        rmp_list = Rmp.objects.all()

        rmp_update = False
        while True:
            play_now = False
            for data in rmp_list:
                if data.now == 0:
                    play_now = True
                    break

            if rmp_list and not play_now:
                for data in rmp_list:
                    if 0 < data.now:
                        data.now -= 1
                        rmp_update = True
            else:
                break

        if rmp_update:
            for data in rmp_list:
                data.save()

        return rmp_list
