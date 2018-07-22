# coding=utf-8
import requests
import re
from requests_oauthlib import OAuth1
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
        if serializer.validated_data['file'] == rmp.file:
            serializer.save()
            if rmp.repeat < serializer.initial_data['repeat']:
                rank, total = self.get_ranking(rmp)
                header = '#NowPlaying My favorite song (%4d/%4d) : ' % (rank, total)
                url = 'https://api.twitter.com/1.1/statuses/update.json'
                auth = OAuth1('conLX2R3H4YcACfiHlgXxRmXX',
                              'vtIzbAelUtCWEmozRU1wczZkYjRGHzbSsLoHGxzsHQG59KfldO',
                              '94802117-HsUE95ZnUmC1frrAJzZjgx2VwDT9VvKrTg68JMuRH',
                              'X0Jzcv0OVAhHLWCcGSe9lA5u4b1ty70DSrfrPdbvk0Ccg')
                song = serializer.initial_data['file'].rstrip('.m4a')
                song = re.sub(r'\/[\d-]+ ', '/', song)
                song = re.sub(r'\/', ' / ', song)
                payload = {'status': header + song}
                requests.post(url, auth=auth, data=payload)
        else:
            raise ValidationError('Mismatch ID? %s %d %d %d'
                                  % (rmp.file, rmp.id, rmp.count, rmp.skip))

    def get_ranking(self, target_rmp):
        rmp_datalist = Rmp.objects.all()
        sorted_rmp_data_list = sorted(rmp_data_list,
                                      key=lambda rmp: rmp.score,
                                      reverse=True)
        for i, rmp in enumerate(sorted_rmp_data_list):
            if rmp.id == target_rmp.id:
                return (i + 1, len(sorted_rmp_data_list))

        raise ValidationError('Mismatch ID? %s'
                              % (rmp.file, rmp.id))

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
