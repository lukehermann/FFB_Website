import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
import time
from espn_api.football import League

from FFB_Website.models import BoxScore, Settings, ff_League, Team


# Create your views here.
def home(request):


    # Get current Year
    league = League(league_id=206814, year=2021);
    standings = league.standings();
    standings_txt = [f"{pos + 1}: {team.team_name} ({team.wins}-{team.losses})" for \
        pos, team in enumerate(standings)];  
    scoreboard = get_scoreboard_short(league, 4);
    ranking = get_power_rankings(league);
    # Add instance of league to database if it doesn't currently exist
    if(not ff_League.objects.filter(year = league.year).exists() and ff_League.objects.filter(league_id = league.league_id)):
        # Add new league obj to database
        new_league = ff_League(league_id = league.league_id, year = league.year, current_week = league.current_week, nfl_week = league.nfl_week)
        new_league.save()

        # Add the league's settings to database
        new_settings = league.settings;
        # print(datetime.datetime.fromtimestamp(new_settings.trade_deadline))
        league_settings = Settings(reg_season_count = new_settings.reg_season_count, veto_votes_required = new_settings.veto_votes_required, team_count = new_settings.team_count, playoff_team_count = new_settings.playoff_team_count, keeper_count = new_settings.keeper_count, name = new_settings.name, tie_rule = (None if new_settings.tie_rule == None else 0), league = new_league)
        league_settings.save();

        # Add Teams to database, connected one to one with league
        for team in league.teams:
            new_team = Team(team_id = team.team_id, team_abbrev = team.team_abbrev, team_name = team.team_name, division_id = team.division_id, division_name = team.division_name, wins = team.wins, losses = team.losses, ties = team.ties, points_for = team.points_for, points_against = team.points_against, owner = team.owner, streak_type = team.streak_type, streak_length = team.streak_length, standing = team.standing, final_standing = team.final_standing, logo_url = team.logo_url)
            new_team.save()

        for i in range(1, league.current_week):
            box_scores = league.box_scores(week=i)
            for box_score in box_scores:
                print(box_score)
                new_box_score = BoxScore(home_team = Team.objects.get(team_id = box_score.home_team.team_id), home_score =  box_score.home_score, home_projected = box_score.home_projected, away_team = Team.objects.get(team_id = box_score.away_team.team_id), away_score = box_score.away_score, away_projected = box_score.away_projected)
                new_box_score.save()
    score = league.box_scores();
    print(score[1].home_team.team_name)

    return render(request, 'home.html', {'league': standings_txt, 'scoreboard': score, 'ranking': ranking});  # show the page with all the submissions
    # return HttpResponse("Hello, Django!")



def get_scoreboard_short(league, week=None):
    #Gets current week's scoreboard
    box_scores = league.box_scores(week=week);
    score = ['%s %.2f - %.2f %s' % (i.home_team.team_abbrev, i.home_score,
                i.away_score, i.away_team.team_abbrev) for i in box_scores
                if i.away_team];
    text = ['Score Update'] + score;
    return '\n'.join(text);


def get_power_rankings(league, week=None):
    # power rankings requires an integer value, so this grabs the current week for that
    if not week:
        week = league.current_week;
    #Gets current week's power rankings
    #Using 2 step dominance, as well as a combination of points scored and margin of victory.
    #It's weighted 80/15/5 respectively
    power_rankings = league.power_rankings(week=week);

    score = ['%s - %s' % (i[0], i[1].team_name) for i in power_rankings
                if i];
    text = ['Power Rankings'] + score;
    return '\n'.join(text);


def get_trophies(league, week=None):
    #Gets trophies for highest score, lowest score, closest score, and biggest win
    matchups = league.box_scores(week=week)
    low_score = 9999
    low_team_name = ''
    high_score = -1
    high_team_name = ''
    closest_score = 9999
    close_winner = ''
    close_loser = ''
    biggest_blowout = -1
    blown_out_team_name = ''
    ownerer_team_name = ''

    for i in matchups:
        if i.home_score > high_score:
            high_score = i.home_score
            high_team_name = i.home_team.team_name
        if i.home_score < low_score:
            low_score = i.home_score
            low_team_name = i.home_team.team_name
        if i.away_score > high_score:
            high_score = i.away_score
            high_team_name = i.away_team.team_name
        if i.away_score < low_score:
            low_score = i.away_score
            low_team_name = i.away_team.team_name
        if i.away_score - i.home_score != 0 and \
            abs(i.away_score - i.home_score) < closest_score:
            closest_score = abs(i.away_score - i.home_score)
            if i.away_score - i.home_score < 0:
                close_winner = i.home_team.team_name
                close_loser = i.away_team.team_name
            else:
                close_winner = i.away_team.team_name
                close_loser = i.home_team.team_name
        if abs(i.away_score - i.home_score) > biggest_blowout:
            biggest_blowout = abs(i.away_score - i.home_score)
            if i.away_score - i.home_score < 0:
                ownerer_team_name = i.home_team.team_name
                blown_out_team_name = i.away_team.team_name
            else:
                ownerer_team_name = i.away_team.team_name
                blown_out_team_name = i.home_team.team_name

    low_score_str = ['Low score: %s with %.2f points' % (low_team_name, low_score)]
    high_score_str = ['High score: %s with %.2f points' % (high_team_name, high_score)]
    close_score_str = ['%s barely beat %s by a margin of %.2f' % (close_winner, close_loser, closest_score)]
    blowout_str = ['%s blown out by %s by a margin of %.2f' % (blown_out_team_name, ownerer_team_name, biggest_blowout)]

    text = ['Trophies of the week:'] + low_score_str + high_score_str + close_score_str + blowout_str
    return '\n'.join(text)
