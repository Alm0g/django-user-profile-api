from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles.api.views import (
    ProfileViewSet, 
    ProfileStatusViewSet,
    AvatarUpdateView
)

router = DefaultRouter()
# r is a RAW string
router.register(r'profiles', ProfileViewSet)
router.register(r'status', ProfileStatusViewSet, basename='status')

urlpatterns = [
    path("", include(router.urls)),
    path('avatar/', AvatarUpdateView.as_view(), name='avatar-update')
]