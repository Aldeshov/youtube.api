from django.urls import path, re_path

from content.views import comments, my_comment, my_comments, VideoContentsViewSet, VideoContentViewSet, \
    MyVideoContentViewSet, MyVideoContentsViewSet, PlaylistViewSet, MyPlaylistsViewSet

urlpatterns = [
    path('contents', VideoContentsViewSet.as_view({
        'get': 'list',
        "post": 'create'
    })),
    path('contents/me', MyVideoContentsViewSet.as_view({
        'get': 'list'
    })),
    path('contents/me/<str:code>', MyVideoContentViewSet.as_view({
        'get': 'retrieve',
        "put": 'update',
        'delete': 'destroy'
    })),
    path('contents/<str:code>', VideoContentViewSet.as_view({
        'get': 'retrieve'
    })),
    re_path(r'^contents/(?P<code>\w+)/save(?:undo=(?P<undo>\d+))?$',
            VideoContentViewSet.as_view({'put': 'save'})),
    re_path(r'^contents/(?P<code>\w+)/like(?:dislike=(?P<dislike>\d+)&retract=(?P<retract>\d+))?$',
            VideoContentViewSet.as_view({'put': 'like'})),
    path('contents/<str:code>/comments', comments),
    path('contents/<str:code>/comments/me', my_comments),
    path('contents/<str:code>/comments/me/<int:comment_id>', my_comment),
    path('playlists', PlaylistViewSet.as_view({'post': 'create'})),
    path('playlists/<int:key>', PlaylistViewSet.as_view({'get': 'retrieve'})),
    re_path(r'^playlists/(?P<key>\d+)/save(?:undo=(?P<undo>\d+))?$',
            PlaylistViewSet.as_view({'put': 'save'})),
    path('playlists/me', MyPlaylistsViewSet.as_view({'get': 'list'})),
    path('playlists/me/<int:key>', MyPlaylistsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }))
]
