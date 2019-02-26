from django.contrib.auth.models import User, Group
from rest_framework import serializers

from admin_console.models import DataFile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class DataFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataFile
        fields = '__all__'
