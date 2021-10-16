from django.db import models
from django.db.models.aggregates import Max
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.db.models.fields.related import OneToOneField


# Create your models here.
class ff_League(models.Model):
    league_id = models.IntegerField()
    year = models.IntegerField()
    current_week = models.IntegerField()
    nfl_week = models.IntegerField()

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
    # Trade Deadline epoch int wont convert correctly using dateTime
    # trade_deadline = models.DateTimeField()
    name = models.CharField(max_length=64)
    tie_rule = models.IntegerField(null=True, blank=True)
    playoff_seed_tie_rule = models.IntegerField(null=True, blank=True)
    league = models.OneToOneField(ff_League, on_delete=models.CASCADE)

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
    team_id = models.IntegerField(unique=True)
    team_abbrev = models.CharField(max_length=6)
    team_name = models.CharField(max_length=64)
    division_id = models.CharField(max_length=64)
    division_name = models.CharField(max_length=64)
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    points_for = models.IntegerField()
    points_against = models.IntegerField()
    owner = models.CharField(max_length=64)
    streak_type = models.CharField(max_length=16)
    streak_length = models.IntegerField()
    standing = models.IntegerField()
    final_standing = models.IntegerField()
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
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    home_score = models.IntegerField()
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    away_score = models.IntegerField()
    
# home_team: Team
# home_score: int
# away_team: Team
# away_score: int

class BoxScore(models.Model):
    week = models.IntegerField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='_home_team')
    home_score = models.IntegerField()
    home_projected = models.IntegerField()
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='_away_team')
    away_score = models.IntegerField()
    away_projected = models.IntegerField()
    # home_lineup = 
    # away_lineup = 

# home_team: Team
# home_score: int
# home_projected: int # if it is not the current week this will be -1
# away_team: Team
# away_score: int
# away_projected: int # if it is not the current week this will be -1
# home_lineup: List[BoxPlayer]
# away_lineup: List[BoxPlayer]

class Player(models.Model):
    name = models.CharField(max_length=256)
    playerID = models.IntegerField()
    posRank = models.IntegerField()
    # eligibleSlots 
    acquisitionType = models.CharField(max_length=64)
    proTeam = models.CharField(max_length=6)
    position = models.CharField(max_length=64)
    injuryStatus = models.CharField(max_length=64)
    injured = models.BooleanField()
    total_points = models.IntegerField()
    projected_total_points = models.IntegerField()
    # stats = 



# name: str
# playerId: int
# posRank: int # players positional rank
# eligibleSlots: List[str] # example ['WR', 'WR/TE/RB']
# acquisitionType: str
# proTeam: str # 'PIT' or 'LAR'
# position: str # main position like 'TE' or 'QB'
# injuryStatus: str
# injured: boolean
# total_points: int # players total points during the season
# projected_total_points: int # projected player points for the season
# stats: dict # holds each week stats, actual and projected points. 
# # week 1 example {1: {'breakdown': {'receivingReceptions': 1.7, 'rushingYards': 7.9}, 'points': 14.57, 'projected_points': 24.64, 'projected_breakdown': {'receivingReceptions': 6.354896833, 'rushingYards': 7.890957077}}}
