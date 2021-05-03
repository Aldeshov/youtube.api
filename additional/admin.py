from django.contrib import admin

from additional.models import GameCopyright, SongCopyright, Restrictions

admin.site.register(GameCopyright)
admin.site.register(SongCopyright)
admin.site.register(Restrictions)
