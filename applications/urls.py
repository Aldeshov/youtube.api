from django.urls import path, re_path

from applications.views import ChannelsViewSet, ChannelViewSet, MyChannelViewSet
from content.views import StatusViewSet, MyStatusViewSet

urlpatterns = [
    path('channels', ChannelsViewSet.as_view(
        {
            'post': 'create',
            'get': 'list'
        }
    )),
    path('channels/me', MyChannelViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        }
    )),
    path('channels/me/status', MyStatusViewSet.as_view(
        {
            'post': 'create',
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        }
    )),
    path('channels/<str:code>', ChannelViewSet.as_view(
        {
            'get': 'retrieve',
        }
    )),
    path('channels/<str:code>/status', StatusViewSet.as_view({'get': 'retrieve'})),
    re_path(r'^channels/(?P<code>\w+)/subscribe(?:undo=(?P<undo>\d+))?$',
            ChannelViewSet.as_view({'put': 'subscribe'})),
    path('channels/<str:code>/subscribe/status', ChannelViewSet.as_view({'get': 'subscribe_status'}))
]
