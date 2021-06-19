# from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from profiles.models import Profile


class FriendSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','friends','user')
        # exclude = ('slug','updated','created')



   







        