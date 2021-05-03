from django.urls import path

from additional.views import GameCopyrightViewSet, SongCopyrightViewSet, \
    GameCopyrightItem, SongCopyrightItem, RestrictionsViewSet

urlpatterns = [
    path('copyrights/game', GameCopyrightViewSet.as_view(
        {
            'post': 'create',
            'get': 'list'
        }
    )),
    path('copyrights/game/<int:key>', GameCopyrightItem.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        }
    )),
    path('copyrights/song', SongCopyrightViewSet.as_view(
        {
            'post': 'create',
            'get': 'list'
        }
    )),
    path('copyrights/song/<int:key>', SongCopyrightItem.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        }
    )),
    path('restrictions', RestrictionsViewSet.as_view(
        {
            'post': 'create',
            'get': 'list'
        }
    )),
    path('restrictions/<int:pk>', RestrictionsViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        }
    ))
]
