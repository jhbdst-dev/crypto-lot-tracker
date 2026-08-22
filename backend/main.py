class Team:

    def __init__(self, name):
        self.name = name

    def introduce_team(self):
        print(self.name)

class Player:

    def __init__(self, name, xp, team):
        self.name = name
        self.xp = xp
        self.team = team

    def introduce_players(self):
        print(self.name, self.xp, self.team.name)

team_x = Team("Team X")
team_z = Team("Team Z")

nico = Player("Nico", 1000, team_x)
lynn = Player("Lynn", 1500, team_z)

team_x.introduce_team()
team_z.introduce_team()

nico.introduce_players()
lynn.introduce_players()

"""
def create_player(name, xp, team):
    return {
        "name": name,
        "XP": xp,
        "team": team
    }
    
def introduce_player(player):
    name = player["name"]
    team = player["team"]

    print(f"Hello {name}, you are {team}")

introduce_player(nico)

nico = create_player("Nico", 1000, "Team X")
lynn = create_player("Lynn", 1500, "Team A")

teams = {
    "Team X" : [nico],
    "Team A" : [lynn] 
}


"""