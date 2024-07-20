# Imports
import nfl_data_py as nfl #Main library used for accessing NFL data
import matplotlib.pyplot as plt #Used for more dynamic visualization
import pandas as pd #Main library used for storing, manipulating, and processing data
pd.set_option('display.max_columns', None) #Allow more pa ndas dataframes to be shown during prints
from tqdm import tqdm #Used to display a progress bar during length dataframe operations
tqdm.pandas() #Necessary function for using with pandas

# Set range for years to save CVs of (where first_year is inclusive, and last_year is exclusive)
first_year = 2004
last_year = 2024

# Import raw PBP data
print("\nPBP Data Importing . . .\n") #Print status update
pbp = nfl.import_pbp_data(range(first_year,last_year)) #Built in function collecting raw pbp data within year range
pbp = pbp[pbp["season_type"].isin(["REG"])].reset_index(drop=True) #Only take data from regular season (no post season)
pbp["year"] = pbp["game_id"].str[:4] #Use substring of game_id to create new column "year"
pbp["year"] = pbp["year"].astype(int) #Cast all elements of new column to int (rather than string)
print("\nPBP Data Imported!\n") #Print status update

# Import raw weekly data
print("Weekly Data Importing . . .\n") #Print status update
weekly = nfl.import_weekly_data(range(first_year,last_year)) #Built in function collecting raw weekly data within year range
weekly = weekly[weekly["season_type"].isin(["REG"])].reset_index(drop=True) #Only take data from regular season (no post season)
weekly[0:5] #Print sample of result
print("\nWeekly Data Imported!\n") #Print status update

# Function to lookup opposing team given weekly data
def date_and_team_to_other_team_vectorized(row, pbp):
    # Subset pbp DataFrame based on 'season' and 'week'
    curr_game = pbp[(pbp['year'] == row['season']) & (pbp['week'] == row['week'])]

    # Identify rows where the team is the away team
    away_team_rows = curr_game['away_team'] == row['recent_team']
    if away_team_rows.any():
        return curr_game.loc[away_team_rows, 'home_team'].iloc[0]

    # Identify rows where the team is the home team
    home_team_rows = curr_game['home_team'] == row['recent_team']
    if home_team_rows.any():
        return curr_game.loc[home_team_rows, 'away_team'].iloc[0]

    # Return an empty string if no match is found (bye week)
    return ''

# Call function (using TQDM to show progress)
# TODO: FIND WAY TO SPEED UP, its really slow currently, there must be a better way to do it
print("Opposing Team Lookup . . .") #Print status update
tqdm.pandas()
weekly['opponent_team'] = weekly.progress_apply(date_and_team_to_other_team_vectorized, args=(pbp,), axis=1)
print("Opposing Team Lookup Complete! Sample output:\n") #Print status update
#print(weekly.head()) #Print sample of result

# Create QB DF
print("QB Data Importing . . .\n") #Print status update
qb = weekly[weekly["position"].isin(["QB"])].reset_index(drop=True) #Create new dataframe for relevant QB information
qb["label"] = qb.progress_apply(lambda row: row["player_id"] + ":" + str(row["season"]) + ":" + str(row["week"]).zfill(2) + ":" + row["recent_team"] + ":" + row["opponent_team"], axis=1)
qb = qb.loc[:, ["label",
                "completions",
                "attempts",
                "passing_yards",
                "passing_tds",
                "interceptions",
                "sacks",
                "sack_fumbles",
                "passing_air_yards",
                "passing_yards_after_catch",
                "passing_first_downs",
                "passing_epa",
                "passing_2pt_conversions",
                "pacr",
                "dakota",
                "carries",
                "rushing_yards",
                "rushing_tds",
                "rushing_fumbles",
                "rushing_first_downs",
                "rushing_epa",
                "rushing_2pt_conversions",
                "fantasy_points"]]
print("\nQB Data Imported!\n") #Print status update
qb.to_csv("data\qb.csv", index=False) #Save QB data to CSV

# Create RB DF
print("RB Data Importing . . .\n") #Print status update
rb = weekly[weekly["position"].isin(["RB"])].reset_index(drop=True) #Create new dataframe for relevant RB information
rb["label"] = rb.progress_apply(lambda row: row["player_id"] + ":" + str(row["season"]) + ":" + str(row["week"]).zfill(2) + ":" + row["recent_team"] + ":" + row["opponent_team"], axis=1)
rb = rb.loc[:, ["label",
                "carries",
                "rushing_yards",
                "rushing_tds",
                "rushing_fumbles",
                "rushing_first_downs",
                "rushing_epa",
                "rushing_2pt_conversions",
                "receptions",
                "targets",
                "receiving_yards",
                "receiving_tds",
                "receiving_fumbles",
                "receiving_air_yards",
                "receiving_yards_after_catch",
                "receiving_first_downs",
                "receiving_epa",
                "receiving_2pt_conversions",
                "racr",
                "target_share",
                "air_yards_share",
                "wopr",
                "special_teams_tds",
                "fantasy_points_ppr"]]
print("\nRB Data Imported!\n") #Print status update
rb.to_csv("data\\rb.csv", index=False) #Save RB data to CSV

# Create WR DF
print("WR Data Importing . . .\n") #Print status update
wr = weekly[weekly["position"].isin(["WR"])].reset_index(drop=True) #Create new dataframe for relevant WR information
wr["label"] = wr.progress_apply(lambda row: row["player_id"] + ":" + str(row["season"]) + ":" + str(row["week"]).zfill(2) + ":" + row["recent_team"] + ":" + row["opponent_team"], axis=1)
wr = wr.loc[:, ["label",
                "receptions",
                "targets",
                "receiving_yards",
                "receiving_tds",
                "receiving_fumbles",
                "receiving_air_yards",
                "receiving_yards_after_catch",
                "receiving_first_downs",
                "receiving_epa",
                "receiving_2pt_conversions",
                "racr",
                "target_share",
                "air_yards_share",
                "wopr",
                "special_teams_tds", 
                "fantasy_points",
                "fantasy_points_ppr"]]
print("\nWR Data Imported!\n") #Print status update
wr.to_csv("data\wr.csv", index=False) #Save WR data to CSV

# Create TE DF
print("TE Data Importing . . .\n") #Print status update
te = weekly[weekly["position"].isin(["TE"])].reset_index(drop=True) #Create new dataframe for relevant TE information
te["label"] = te.progress_apply(lambda row: row["player_id"] + ":" + str(row["season"]) + ":" + str(row["week"]).zfill(2) + ":" + row["recent_team"] + ":" + row["opponent_team"], axis=1)
te = te.loc[:, ["label",
                "receptions",
                "targets",
                "receiving_yards",
                "receiving_tds",
                "receiving_fumbles",
                "receiving_air_yards",
                "receiving_yards_after_catch",
                "receiving_first_downs",
                "receiving_epa",
                "receiving_2pt_conversions",
                "racr",
                "target_share",
                "air_yards_share",
                "wopr",
                "special_teams_tds", 
                "fantasy_points",
                "fantasy_points_ppr"]]
print("\nTE Data Imported!\n") #Print status update
te.to_csv("data\\te.csv", index=False) #Save TE data to CSV'''

# Create K DF (more involved since it must use pbp data)
print("K Data Importing . . .\n") #Print status update
roster = nfl.import_seasonal_rosters(range(first_year,last_year)) #Built in function collecting raw roster data within year range
roster = roster[roster["depth_chart_position"].isin(["K"])].reset_index(drop=True) #Only take data from desired positions
roster = roster.loc[:, ["season",
                        "team",
                        "week",
                        "player_id"]]
roster #Print sample of results

#Modular so it can be adjusted depending on league settings
def kicker_fg_fantasy_points(made, dist):
    if made:
        if dist>=50:
            return 5
        return 3
    return 0
def kicker_ep_fantasy_points(made):
    if made:
        return 1
    return 0

k_pbp = pbp[pbp["play_type"].isin(["field_goal","extra_point"])].reset_index(drop=True) #Create new dataframe for relevant K information
k_pbp = k_pbp[k_pbp["season_type"].isin(["REG"])]
k_pbp = k_pbp.loc[:, ["kicker_player_id",
                    "week",
                    "season",
                    "posteam",
                    "defteam",
                    "play_type",
                    "kick_distance",
                    "field_goal_result",
                    "extra_point_result"]]
#print((k_pbp["posteam"]))
unique_kickers = k_pbp["kicker_player_id"].unique()

kick_dict = {}

for x in unique_kickers:

    season = last_year-1 #Upper bound for season year
    week=18 #Upper bound for week in season
    
    while(season>=first_year): #Not exceeding accepted range
        
        while(week>0): #Not exceeding accepted week
            
            curr_kick = k_pbp[k_pbp["week"].isin([week])] #Isolate pbp data to only the week of the game currently being played
            #print("Week Filter:" + str(curr_kick))
            curr_kick = curr_kick[curr_kick["season"].isin([season])] #Isolate pbp data to only the year of the game currently being played
            #print("Season Filter:" + str(curr_kick))
            curr_kick = curr_kick[curr_kick["kicker_player_id"].isin([x])].reset_index(drop=True) #Isolate pbp data to only when the kicker is the input player id
            #print("ID Filter:" + str(curr_kick))
            
            if(not curr_kick.empty):

                #print(curr_kick)

                possession_team = curr_kick["posteam"].at[0]

                defending_team = curr_kick["defteam"].at[0]
                
                fgs = curr_kick[curr_kick["play_type"].isin(["field_goal"])].reset_index(drop=True)
                eps = curr_kick[curr_kick["play_type"].isin(["extra_point"])].reset_index(drop=True)
    
                fgs["field_goal_result"] = fgs.apply(lambda row: row["field_goal_result"]=="made", axis=1)
                eps["extra_point_result"] = eps.apply(lambda row: row["extra_point_result"]=="good", axis=1)
    
                season_num = curr_kick.at[0,"season"]
                week_num = curr_kick.at[0,"week"]
                num_fgs = len(fgs)
                num_eps = len(eps)
                avg_fg_dist = fgs["kick_distance"].mean()
                
                
    
                if len(fgs)!=0:
                    fg_pctg = fgs["field_goal_result"].sum()/len(fgs)
                else:
                    fg_pctg=0
                    
                if len(eps)!=0:
                    ep_pctg = eps["extra_point_result"].sum()/len(eps)
                else:
                    ep_pctg=0
    
                fgs["fantasy_points"] = fgs.apply(lambda row: kicker_fg_fantasy_points(row["field_goal_result"],row["kick_distance"]), axis=1)
                eps["fantasy_points"] = eps.apply(lambda row: kicker_ep_fantasy_points(row["extra_point_result"]), axis=1)
    
                fantasy_points = fgs["fantasy_points"].sum() + eps["fantasy_points"].sum()

                new_id = f"{x}:{str(week)}:{str(season)}:{str(possession_team)}:{str(defending_team)}"

                kick_dict[new_id] = [new_id,len(fgs),len(eps),avg_fg_dist,fg_pctg,ep_pctg,fantasy_points]
                
    
            week-=1 #Repeat inner loop with data from a week ago  
    
        week=18 #Reset week counter
        season-=1 #Repeat outer loop with data from a season ago 

k = pd.DataFrame.from_dict(kick_dict,orient="index")
k = k.rename(columns={0:"label",1:"num_fgs",2:"num_eps",3:"avg_fg_dist",4:"fg_pctg",5:"ep_pctg",6:"fantasy_points"})
print("\nK Data Imported!\n") #Print status update
k.to_csv("data\k.csv", index=False) #Save K data to CSV

def get_defensive_performance_history(team):
    
    season = last_year-1 #Upper bound for season year
    week=18 #Upper bound for week in season

    #pd.DataFrame(data={'season': season_num, 'week': week_num, 'defending_team': defending_team, 'offensive_team': offensive_team, 'interceptions': interceptions, 'sacks': sacks, 'sack_yards': sack_yards, 'sack_fumbles': sack_fumbles, 'sack_fumbles_recovered': sack_fumbles_recovered, 'receiving_fumbles': receiving_fumbles, 'receiving_fumbles_recovered': receiving_fumbles_recovered, 'rushing_yards_allowed': rushing_yards_allowed, 'passing_yards_allowed': passing_yards_allowed, 'passing_tds_allowed': passing_tds_allowed, 'rushing_tds_allowed': rushing_tds_allowed, 'special_teams_tds_allowed': special_teams_tds_allowed},index=[f'{season_num}-{week_num}-{defending_team}'])
    return_df = pd.DataFrame(columns=["season","week","defending_team","offensive_team","interceptions","sacks","sack_yards","sack_fumbles","sack_fumbles_recovered","receiving_fumbles","receiving_fumbles_recovered","rushing_yards_allowed","passing_yards_allowed","passing_tds_allowed","rushing_tds_allowed","special_teams_tds_allowed"])
    #display(return_df)

    while(season>=first_year): #Not exceeding accepted range
        
        while(week>0): #Not exceeding accepted week
            
            curr_week = weekly[weekly["week"].isin([week])] #Isolate weekly data to only the week of the game currently being played
            curr_week = curr_week[curr_week["season"].isin([season])] #Isolate weekly data to only the year of the game currently being played
            curr_week = curr_week[curr_week["opponent_team"].isin([team])].reset_index(drop=True) #Isolate weekly data to only when the defending team is the input team

            #display(curr_week)
            
            #Construct dataset using weekly data for current week, season, and defending team
            #Note: opponents stats now reflect the defensive performance, just inverted (E.G. rushing_yards now is rushing_yards allowed)
            if not curr_week.empty:
                season_num = curr_week.at[0,"season"]
                #print(season_num)
                week_num = curr_week.at[0,"week"]
                defending_team = curr_week.at[0,"opponent_team"]
                offensive_team = curr_week.at[0,"recent_team"]
                interceptions = curr_week[["interceptions"]].sum().iloc[0]
                sacks = curr_week[["sacks"]].sum().iloc[0]
                sack_yards = curr_week[["sack_yards"]].sum().iloc[0]
                sack_fumbles = curr_week[["sack_fumbles"]].sum().iloc[0]
                sack_fumbles_recovered = curr_week[["sack_fumbles_lost"]].sum().iloc[0]
                receiving_fumbles = curr_week[["receiving_fumbles"]].sum().iloc[0]
                receiving_fumbles_recovered = curr_week[["receiving_fumbles_lost"]].sum().iloc[0]
                rushing_yards_allowed = curr_week[["rushing_yards"]].sum().iloc[0]
                passing_yards_allowed = curr_week[["passing_yards"]].sum().iloc[0]
                passing_tds_allowed = curr_week[["passing_tds"]].sum().iloc[0]
                rushing_tds_allowed = curr_week[["rushing_tds"]].sum().iloc[0]
                special_teams_tds_allowed = curr_week[["special_teams_tds"]].sum().iloc[0]
                new_df = pd.DataFrame(data={'season': season_num, 'week': week_num, 'defending_team': defending_team, 'offensive_team': offensive_team, 'interceptions': interceptions, 'sacks': sacks, 'sack_yards': sack_yards, 'sack_fumbles': sack_fumbles, 'sack_fumbles_recovered': sack_fumbles_recovered, 'receiving_fumbles': receiving_fumbles, 'receiving_fumbles_recovered': receiving_fumbles_recovered, 'rushing_yards_allowed': rushing_yards_allowed, 'passing_yards_allowed': passing_yards_allowed, 'passing_tds_allowed': passing_tds_allowed, 'rushing_tds_allowed': rushing_tds_allowed, 'special_teams_tds_allowed': special_teams_tds_allowed},index=[f'{season_num}-{week_num}-{defending_team}'])
                return_df = pd.concat([return_df,new_df])
                #display(return_df)
                
            week-=1 #Repeat inner loop with data from a week ago  
            
        week=18 #Reset week counter
        season-=1 #Repeat outer loop with data from a season ago  
        
    return return_df #Array with appended data from all defensive activities

#Empty array for each team abbreviation
team_defenses = [
    "NE",
    "NO",
    "NYJ",
    "LAC",
    "ATL",
    "NYG",
    "ARI",
    "PIT",
    "WAS",
    "GB",
    "MIA",
    "PHI",
    "BUF",
    "DET",
    "TB",
    "SEA",
    "TEN",
    "BAL",
    "LV",
    "SF",
    "CAR",
    "KC",
    "JAX",
    "CHI",
    "LA",
    "DEN",
    "HOU",
    "CIN",
    "MIN",
    "CLE",
    "IND",
    "DAL"
]

return_df = pd.DataFrame(columns=["season","week","defending_team","offensive_team","interceptions","sacks","sack_yards","sack_fumbles","sack_fumbles_recovered","receiving_fumbles","receiving_fumbles_recovered","rushing_yards_allowed","passing_yards_allowed","passing_tds_allowed","rushing_tds_allowed","special_teams_tds_allowed"])

#Populate dictionary with cooresponding team's history of defensive performances
for x in team_defenses:
    #Create dataframe from dictionary
    d = get_defensive_performance_history(x)
    return_df = pd.concat([return_df,d])
    
print("\nD Data Imported!\n") #Print status update
return_df.to_csv(f"data\d.csv", index=False) #Save D data to CSV