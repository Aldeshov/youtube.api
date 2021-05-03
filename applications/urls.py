from django.urls import path

from applications.views import ChannelsViewSet, ChannelViewSet, MyChannelViewSet

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
    path('channels/<str:code>', ChannelViewSet.as_view(
        {
            'get': 'retrieve',
        }
    ))
]
