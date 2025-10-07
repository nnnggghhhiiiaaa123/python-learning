from requests import get, exceptions
from pprint import PrettyPrinter
import urllib3

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

printer = PrettyPrinter()

# Helper that retries with verify=False on SSLError
def safe_get(url, timeout=10):
    try:
        return get(url, timeout=timeout)
    except exceptions.SSLError:
        # fallback: disable warnings and retry without verifying certs
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return get(url, timeout=timeout, verify=False)
    except exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_links():
    resp = safe_get(BASE_URL + ALL_JSON)
    if not resp:
        return {}
    try:
        data = resp.json()
    except ValueError:
        print("Failed to decode JSON from today.json")
        return {}
    return data.get('links', {})

def get_scoreboard():
    links = get_links()
    scoreboard = links.get('currentScoreboard')
    if not scoreboard:
        print("No currentScoreboard link available")
        return

    resp = safe_get(BASE_URL + scoreboard)
    if not resp:
        return
    try:
        games = resp.json().get('games', [])
    except ValueError:
        print("Failed to decode scoreboard JSON")
        return

    for game in games:
        home_team = game.get('hTeam', {})
        away_team = game.get('vTeam', {})
        clock = game.get('clock', '')
        period = game.get('period', {}).get('current', '')

        print("-------------------------------------------------")
        print(f"{home_team.get('triCode', '')} vs {away_team.get('triCode', '')}")
        print(f"{home_team.get('score', '')} vs {away_team.get('score', '')}")
        print(f"{clock}, {period}")

def get_stats():
    links = get_links()
    stats_link = links.get('leagueGameStatsLeaders')
    if not stats_link:
        print("No leagueGameStatsLeaders link available")
        return

    resp = safe_get(BASE_URL + stats_link)
    if not resp:
        return

    try:
        data = resp.json()
    except ValueError:
        print("Failed to decode stats JSON")
        return

    # navigate safely to teams list
    teams = data.get('league', {}).get('standard', {}).get('regularSeason', {}).get('teams', [])
    if not teams:
        print("No teams data found in stats response")
        return

    teams = [t for t in teams if t.get('name') != "Team"]
    def ppg_rank_key(x):
        try:
            return int(x.get('ppg', {}).get('rank', 9999))
        except (TypeError, ValueError):
            return 9999

    teams.sort(key=ppg_rank_key)

    for i, team in enumerate(teams):
        name = team.get('name', '')
        nickname = team.get('nickname', '')
        ppg = team.get('ppg', {}).get('avg', '')
        print(f"{i + 1}. {name} - {nickname} - {ppg}")

if __name__ == "__main__":
    # call the function you want
    get_stats()