def print_outcomes(players):
    for k in players:
        print(str(k.get_player_name() + " Scaled W/L ") +  str(k.get_winloss()) + " Normal W/L "  + str(k.get_wl()))

def players_swap(swap1,swap2):
    return swap2, swap1

def list_players(input_players_list, name):
    list_players = len(input_players_list)
    print("\nTeam Name: " + str(name))
    for k in range(0,list_players):
        input_players_list[k].display_object()
    print("\n")
    

def partition_teams(input_players_list):
    plyers_number = len(input_players_list)
    left_team = []
    right_team = []
    for k in range(0,plyers_number-(plyers_number % 2) ): #if even number of players, just partitions into halfs,if odd number of players, partitions into two even teams and ignores highest ranked player.
        if k % 2 == 0: #is even 
            right_team.append(input_players_list[k])
        else:
            left_team.append(input_players_list[k])
    #this segment just assigns the highest rated player to the team with the worst total competence, not average competence, total competence, if the team numbers are odd
    if((plyers_number % 2) != 0):
        left_competence = 0
        for j1 in left_team:
            left_competence = left_competence + j1.get_winloss()
        right_competence = 0
        for j2 in right_team:
            right_competence = right_competence + j2.get_winloss()
        if(left_competence > right_competence):
            right_team.append(input_players_list[plyers_number-1]) 
        else:
            left_team.append(input_players_list[plyers_number-1])
    return left_team, right_team


def check_player_sort(input_players_list):
    ply_list = input_players_list
    num_plyers = len(ply_list)
    sorted_check = True
    for plyer_index in range(0,num_plyers-1):
        #print("Results:", ply_list[plyer_index].display_object(), ply_list[plyer_index+1].display_object(), plyer_index)
        if(ply_list[plyer_index].get_winloss() <= ply_list[plyer_index+1].get_winloss()):
            sorted_check = True
        else:
            return False
    return True

def players_sort(input_players_list):
    ply_list = input_players_list
    num_plyers = len(ply_list)
    Try_Sort = True
    while(Try_Sort):
        for plyer_index in range(0,num_plyers-1):
            if(ply_list[plyer_index].get_winloss() > ply_list[plyer_index+1].get_winloss()):
                #print("Triggered:", ply_list[plyer_index].display_object(), ply_list[plyer_index+1].display_object())
                ply_list[plyer_index], ply_list[plyer_index+1] = players_swap(ply_list[plyer_index], ply_list[plyer_index+1])
        Try_Sort = not check_player_sort(ply_list)
    return ply_list

def suggest_teams(teams_list):
    sorted_teams_list = players_sort(teams_list)
    team1, team2 = partition_teams(sorted_teams_list)
    list_players(team1, "Suggested Red Team")
    list_players(team2, "Suggested Blue Team")
        
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
    
    def display_object(self):
        print(self.get_player_name(), self.get_winloss(), self.get_wl())
    
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

"""

"""


Cole     = Player("Cole")
Saterk   = Player("Saterk")
Poldi    = Player("Poldi")
Tazzy    = Player("Tazzy")
Chikanhu = Player("Chikanhu")
Darthon  = Player("Darthon")
Bret     = Player("Bret")
PLAYERS = [ Cole, Saterk, Poldi, Tazzy, Chikanhu, Darthon, Bret]
CURRENT_MATCH = []


'''
Various Commands
'''
#left [ ] is one team, right [ ] is another team, 1 signals left [ ] won the round, -1 signals right [ ] won, 0 indicates a draw
#Match0   = MatchRound( [Tazzy, Saterk, Poldi]  , [Cole, Chikanhu, Darthon],    0) 
#Match0.update_teams() would be used to update rankings
#print_outcomes(PLAYERS) would be display rankings, no sorting
#players_sort(PLAYERS) would be to sort player rankings
#suggest_teams(PLAYERS) suggest teams based on total player pools
#suggest_teams(PLAYERS[0:x] + PLAYERS[y,z]) suggest teams based subset of total player pools broken into two groups, can use multiple + to look at different players

#Previous Fights Logs
Match0   = MatchRound( [Tazzy, Saterk, Poldi]  , [Cole, Chikanhu, Darthon],    0)
Match0.update_teams()
Match1   = MatchRound( [Tazzy, Poldi, Chikanhu]  , [Cole, Bret, Darthon],    0)
Match1.update_teams()

#update CURRENT_MATCH to be the list of all players competing in the current round
CURRENT_MATCH = PLAYERS
suggest_teams(CURRENT_MATCH)
