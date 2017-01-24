from django.contrib import admin
from models import Point,UserScore

class PointAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_name', 'action_date', 'points_earned')

class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'xscore', 'score_rank', 'xscore_rank')

admin.site.register(Point, PointAdmin)
admin.site.register(UserScore, UserScoreAdmin)
