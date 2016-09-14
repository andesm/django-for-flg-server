from django.contrib.auth.models import User
from rest_framework import serializers
from rmp.models import Rmp

class RmpSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Rmp
        fields = ('id', 'owner', 'site', 'file', 'source', 'image', 'genre',
                  'album','artist', 'title', 'duration', 'trackNumber',
                  'totalTrackCount', 'now', 'count', 'skip', 'repeat',
                  'score')


class UserSerializer(serializers.ModelSerializer):
    rmps = serializers.PrimaryKeyRelatedField(many=True, queryset=Rmp.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'rmps')

       
