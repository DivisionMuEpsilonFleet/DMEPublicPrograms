class Player:
    Wins = 0
    Losses = 0
    WeightedWins   = 0
    WeightedLosses = 0


    def __init__(self, wins, losses,wwins,wlosses):
        self.Wins           = wins
        self.Losses         = losses
        self.WeightedWins   = wwins
        self.WeightedLosses = wlosses
    

    """
    Using outcome as 1 if it was a win, -1 if a loss, 0 is a tie
    """
    def update_player(self, outcome, enemy_comptence_multiplier,team_competence_multiplier):
        self.Wins              = self.Wins +        outcome
        self.Losses            = self.Wins + (-1) * outcome
        self.WeightedWins      = self.Wins +        outcome * (enemy_comptence_multiplier / team_competence_multiplier)
        self.WeightedLosses    = self.Wins + (-1) * outcome * (enemy_comptence_multiplier / team_competence_multiplier)

    def get_winloss(self):
        return (self.WeightedWins)/(self.WeightedLosses)

class MatchRound:
    red_team    = []
    blue_team   = []
    red_deaths  = []
    blue_deaths = []
    OutcomeValue = 0 #1 for red team, -1 for blue team, 0 if a tie

    def __init__(self, red_team, blue_team,red_deaths,blue_deaths, OutcomeValue):
        self.red_team     = red_team
        self.blue_team    = blue_team
        self.red_deaths   = red_deaths
        self.blue_deaths  = blue_deaths
        self.OutcomeValue = OutcomeValue

    def calculate_mean_team_competence(self):
        red_team_size = len(self.red_team)
        red_team_competence = 0 #starting value
        for red_player in range(0, red_team_size):
            red_team_competence = red_team_competence + red_player.get_winloss()
        red_team_competence = red_team_competence / red_team_size #this is the mean competence of the red team

        blue_team_size = len(self.blue_team)
        blue_team_competence = 0 #starting value
        for blue_player in range(0,blue_team_size):
            blue_team_competence = blue_team_competence + blue_player.get_winloss()
        blue_team_competence = blue_team_competence / blue_team_size #this is the mean competence of the blue team

        return red_team_competence, blue_team_competence


    def update_teams(self):
        red_team_competence, blue_team_competence = self.calculate_mean_team_competence() #calculates mean competence of enemy team
        
        red_team_size = len(self.red_team)
        for red_player in range(0, red_team_size):
            red_player.update_player  ( 1*self.OutcomeValue  , blue_team_competence, red_team_competence)
       
        blue_team_size = len(self.blue_team)
        for blue_player in range(0,blue_team_size):
            blue_player.update_player ( -1*self.OutcomeValue , red_team_competence, blue_team_competence)
