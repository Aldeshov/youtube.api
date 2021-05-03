from django.contrib import admin

from content.models import Playlist, CommunityContent, Status, Content, Comment

admin.site.register(Comment)
admin.site.register(Content)
admin.site.register(Status)
admin.site.register(CommunityContent)
admin.site.register(Playlist)
