from django.shortcuts import render
from django.http import HttpResponse

from espn_api.football import League


# Create your views here.
def home(request):

    league = League(league_id=206814, year=2021, debug=True);
    standings = league.standings();
    standings_txt = [f"{pos + 1}: {team.team_name} ({team.wins}-{team.losses})" for \
        pos, team in enumerate(standings)];  

    scoreboard = get_scoreboard_short(league, 4);

    ranking = get_power_rankings(league);
    return render(request, 'home.html', {'league': standings_txt, 'scoreboard': scoreboard, 'ranking': ranking})  # show the page with all the submissions
    # return HttpResponse("Hello, Django!")



def get_scoreboard_short(league, week=None):
    #Gets current week's scoreboard
    box_scores = league.box_scores(week=week)
    score = ['%s %.2f - %.2f %s' % (i.home_team.team_abbrev, i.home_score,
                i.away_score, i.away_team.team_abbrev) for i in box_scores
                if i.away_team]
    text = ['Score Update'] + score
    return '\n'.join(text)


def get_power_rankings(league, week=None):
    # power rankings requires an integer value, so this grabs the current week for that
    if not week:
        week = league.current_week
    #Gets current week's power rankings
    #Using 2 step dominance, as well as a combination of points scored and margin of victory.
    #It's weighted 80/15/5 respectively
    power_rankings = league.power_rankings(week=week)

    score = ['%s - %s' % (i[0], i[1].team_name) for i in power_rankings
                if i]
    text = ['Power Rankings'] + score
    return '\n'.join(text)