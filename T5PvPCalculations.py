def print_outcomes():
    for k in PLAYERS:
        print(str(k.get_player_name() + " Scaled W/L ") +  str(k.get_winloss()) + " Normal W/L "  + str(k.get_wl()))


class Player:
    Name = ""
    Wins           = 1
    Losses         = 1
    WeightedWins   = 1
    WeightedLosses = 1


    def __init__(self, name):
        self.Name = name
        pass
    

    """
    Using outcome as 1 if it was a win, -1 if a loss, 0 is a tie
    """
    def update_player(self, outcome, enemy_comptence_multiplier,team_competence_multiplier):
        total_games_played = self.Wins + self.Losses

        if(outcome > 0):
            self.Wins           = self.Wins           + 1
            self.WeightedWins   = self.WeightedWins   + 1 * (enemy_comptence_multiplier / team_competence_multiplier)  *  (total_games_played/(total_games_played+2))
        elif(outcome < 0):
            self.Losses         = self.Losses         + 1
            self.WeightedLosses = self.WeightedLosses + 1 * (enemy_comptence_multiplier / team_competence_multiplier)  *  (total_games_played/(total_games_played+2))


    def get_winloss(self):


        return int(1000*(self.WeightedWins)/(self.WeightedLosses))/1000
        
        
    def get_wl(self):
        return int(1000*(self.Wins)/(self.Losses))/1000
        
        
    def get_player_name(self):
        return self.Name
    


class MatchRound:
    red_team    = []
    blue_team   = []
    OutcomeValue = 0 #1 for red team, -1 for blue team, 0 if a tie

    def __init__(self, red_team, blue_team, OutcomeValue):
        self.red_team     = red_team
        self.blue_team    = blue_team
        self.OutcomeValue = OutcomeValue

    def calculate_mean_team_competence(self):
        red_team_size = len(self.red_team)
        red_team_competence = 0 #starting value
        for red_index in range(0, red_team_size):
            red_team_competence = red_team_competence + self.red_team[red_index].get_winloss()
        red_team_competence = red_team_competence / red_team_size #this is the mean competence of the red team

        blue_team_size = len(self.blue_team)
        blue_team_competence = 0 #starting value
        for blue_index in range(0,blue_team_size):
            blue_team_competence = blue_team_competence + self.blue_team[blue_index].get_winloss()
        blue_team_competence = blue_team_competence / blue_team_size #this is the mean competence of the blue team

        return red_team_competence, blue_team_competence


    def update_teams(self):
        red_team_competence, blue_team_competence = self.calculate_mean_team_competence() #calculates mean competence of enemy team
        red_team_size = len(self.red_team)
        for red_index in range(0, red_team_size):
            self.red_team[red_index].update_player  ( 1*self.OutcomeValue  , blue_team_competence, red_team_competence)
       
        blue_team_size = len(self.blue_team)
        for blue_index in range(0,blue_team_size):
            self.blue_team[blue_index].update_player ( -1*self.OutcomeValue , red_team_competence, blue_team_competence)
