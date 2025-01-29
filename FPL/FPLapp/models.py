from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS_CHOICES = (
    ("Available","Available"),
    ("Injured","Injured"),
    ("Suspended","Suspended")
)

class Player(models.Model):
    player_Team=models.CharField(max_length=5)
    player_Name=models.CharField(max_length=30)
    player_Position=models.CharField(max_length=5)
    player_Total_Shots=models.SmallIntegerField()
    player_Goals=models.SmallIntegerField()
    player_Expected_Goals=models.FloatField()
    player_Total_Passes=models.SmallIntegerField()
    player_Assists=models.SmallIntegerField()
    player_Big_Chances_Created=models.SmallIntegerField()
    player_Tackles=models.SmallIntegerField()
    player_Interceptions=models.SmallIntegerField()
    player_Clearances=models.SmallIntegerField()
    player_Saves=models.SmallIntegerField()
    player_High_Claims=models.SmallIntegerField()
    player_Punches=models.SmallIntegerField()
    player_Appearances=models.SmallIntegerField()
    player_Clean_Sheet=models.SmallIntegerField()
    player_Yellow_Cards=models.SmallIntegerField()
    player_Red_Cards=models.SmallIntegerField()
    player_Status=models.CharField(max_length=20, choices=STATUS_CHOICES, default="Availabe")
    player_Rating=models.FloatField()

    def __str__(self):
        return self.name

SQUAD_CHOICES = (
    ("Saved","Saved"),
    ("Not Created","Not Created")
)

class Squad(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    player=models.ForeignKey(Player,on_delete=models.CASCADE)
    squad_Status=models.CharField(max_length=20, choices=SQUAD_CHOICES,default="Not Created")

    def __init__(self):
        return self.id

PLAYER_CHOICES = (
    ("Playing","Playing"),
    ("Bench","Bench")
)

XI_CHOICES = (
    ("Saved","Saved"),
    ("Not Created","Not Created")
)

class XI(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    player=models.ForeignKey(Player,on_delete=models.CASCADE)
    player_Role=models.CharField(max_length=20, choices=PLAYER_CHOICES,default="Bench")
    captain=models.BooleanField(default=False)
    vice_captain=models.BooleanField(default=False)
    xi_Status=models.CharField(max_length=20, choices=XI_CHOICES,default="Not Created")

    def __init__(self):
        return self.id

