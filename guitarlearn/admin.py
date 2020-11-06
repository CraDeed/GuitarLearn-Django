from django.contrib import admin
from .models import YoutubeTutorial, PlayList

@admin.register(YoutubeTutorial)
class YoutubeTutorialAdmin(admin.ModelAdmin):
    pass

@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    pass