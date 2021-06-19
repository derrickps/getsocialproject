from rest_framework import viewsets
from rest_framework import generics
from profiles.models import Profile
from social.api.serializers import FriendSerializer

from rest_framework.permissions import IsAuthenticated


class ProfileVIEWSET(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    queryset = Profile.objects.all()
    search_fields=('first_name','email','mobile')
    permission_classes = [IsAuthenticated,]


class FriendListAPIView(generics.ListAPIView):
    serializer_class = FriendSerializer
    def get_queryset(self):
        qs = Profile.objects.all()
        name = self.request.GET.get('user')
        if name is not None:
            qs = qs.values('friends',)
        return qs