from django.urls import path,include
from rest_framework import routers
from social.api import views

from social.api.views import ProfileVIEWSET
router = routers.DefaultRouter()
router.register('profileapi',ProfileVIEWSET)

urlpatterns = [
    path('', include(router.urls)),
    path('friends/',views.FriendListAPIView.as_view()),
]