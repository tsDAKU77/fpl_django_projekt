from django.contrib import admin
from .models import Player, Squad, XI

# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display=('player_Team',
                  'player_Name', 
                  'player_Position',
                  'player_Total_Shots',
                  'player_Goals',
                  'player_Expected_Goals',
                  'player_Total_Passes',
                  'player_Assists',
                  'player_Big_Chances_Created',
                  'player_Tackles',
                  'player_Interceptions',
                  'player_Clearances',
                  'player_Saves',
                  'player_High_Claims',
                  'player_Punches',
                  'player_Appearances',
                  'player_Clean_Sheet',
                  'player_Yellow_Cards',
                  'player_Red_Cards',
                  'player_Status',
                  'player_Rating')

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display=('id',
                  'username',
                  'player',
                  'squad_Status')

@admin.register(XI)
class XIAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'player',
        'player_Role',
        'captain',
        'vice_captain',
        'xi_Status',      
    )
