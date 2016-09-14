from rmp.models import Rmp
from rmp.serializers import UserSerializer, RmpSerializer 
from rmp.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.exceptions import ParseError

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RmpViewSet(viewsets.ModelViewSet):
    serializer_class = RmpSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        if Rmp.objects.filter(file=serializer.validated_data['file']):
            raise ParseError()
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        list = Rmp.objects.all()

        rmp_update = False
        while True:
            play_now = False
            for data in list:
                if data.now == 0:
                    play_now = True
                    break

            if list and not play_now:
                for data in list:
                    if 0 < data.now:
                        data.now -= 1
                        rmp_update = True
            else:
                break

        if rmp_update:
            list.save()
            
        return list




