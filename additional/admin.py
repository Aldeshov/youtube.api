from django.contrib import admin

from additional.models import GameCopyright, SongCopyright, Copyrights

admin.site.register(GameCopyright)
admin.site.register(SongCopyright)
admin.site.register(Copyrights)
