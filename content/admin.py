from django.contrib import admin

from content.models import Playlist, Status, VideoContent, Comment

admin.site.register(Comment)
admin.site.register(VideoContent)
admin.site.register(Status)
admin.site.register(Playlist)
