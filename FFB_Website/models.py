from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField

# Create your models here.
class League(models.Model):
    league_id = models.IntegerField()
    year = models.IntegerField()
    settings_id = OneToOneField(Settings, on_delete=models.CASCADE, primary_key=true)

# league_id: int
# year: int
# settings: Settings
# teams: List[Team]
# draft: List[Pick]
# current_week: int # current fantasy football week
# nfl_week: int # current nfl week

class Settings(models.Model):
    reg_season_count = models.IntegerField()
    veto_votes_required = models.IntegerField()
    team_count = models.IntegerField()
    playoff_team_count = models.IntegerField()
    keeper_count = models.IntegerField()
    trade_deadline = models.IntegerField()
    name = models.CharField(max_length=64)
    tie_rule = models.IntegerField()
    playoff_seed_tie_rule = models.IntegerField()


#     reg_season_count: int
# veto_votes_required: int
# team_count: int
# playoff_team_count: int
# keeper_count: int
# trade_deadline: int epoch
# name: str
# tie_rule: int
# playoff_seed_tie_rule: int


class Team(models.Model):
    team_id = models.IntegerField()
    team_abbrev = models.CharField(max_length=6)
    team_name = models.CharField(max_length=64)
    division_id = models.CharField(max_length=64)
    division_name = models.CharField(max_length=64)
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    points_for = models.IntegerField()
    points_agaisnt = models.IntegerField()
    owner = models.CharField(max_length=64)
    streak_type = models.CharField(max_length=16)
    streak_length = models.IntegerField()
    standing = models.IntegerField()
    final_standings = models.IntegerField()
    logo_url = models.CharField(max_length=256)


# team_id: int
# team_abbrev: str
# team_name: str
# division_id: str
# division_name: str
# wins: int
# losses: int
# ties: int
# points_for: int # total points for through out the season
# points_against: int # total points against through out the season
# owner: str
# streak_type: str # string of either WIN or LOSS
# streak_length: int # how long the streak is for streak type
# standing: int # standing before playoffs
# final_standings: int # final standing at end of season
# logo_url: str
# roster: List[Player]

# # These 3 variables will have the same index and match on those indexes
# schedule: List[Team]
# scores: List[int]
# outcomes: List[str]




class Matchup(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    away_score = models.IntegerField()
    
# home_team: Team
# home_score: int
# away_team: Team
# away_score: int
