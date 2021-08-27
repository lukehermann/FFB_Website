import os
import requests
from espn_api.football import League

def get_League(self, league_id, year, espn_s2=None, swid=None):
    self.league_id = league_id
    self.year = year
    url = "http://games.espn.com/ffl/api/v2/"
    return 1


def get_droplets():
    url = 'https://api.digitalocean.com/v2/droplets'
    r = requests.get(url, headers={'Authorization':'Bearer %s' % 'access_token'})
    droplets = r.json()
    droplet_list = []
    for i in range(len(droplets['droplets'])):
        droplet_list.append(droplets['droplets'][i])
    return droplet_list