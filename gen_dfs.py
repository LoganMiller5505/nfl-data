# Imports
import nfl_data_py as nfl #Main library used for accessing NFL data
import matplotlib.pyplot as plt #Used for more dynamic visualization
import pandas as pd #Main library used for storing, manipulating, and processing data
pd.set_option('display.max_columns', None) #Allow more pa ndas dataframes to be shown during prints
from tqdm import tqdm #Used to display a progress bar during length dataframe operations
tqdm.pandas() #Necessary function for using with pandas

# Set range for years to save CVs of (where first_year is inclusive, and last_year is exclusive)
first_year = 2012
last_year = 2024

# Import raw NGS data
'''rec_ngs = nfl.import_ngs_data("receiving", range(first_year,last_year))
pass_ngs = nfl.import_ngs_data("passing", range(first_year,last_year))
rush_ngs = nfl.import_ngs_data("rushing", range(first_year,last_year))
rec_ngs.fillna(-1, inplace=True)
pass_ngs.fillna(-1, inplace=True)
rush_ngs.fillna(-1, inplace=True)
print(rec_ngs.head())
print(pass_ngs.head())
print(rush_ngs.head())
rec_ngs.to_csv("misc\\rec_ngs.csv", index=False)
pass_ngs.to_csv("misc\\pass_ngs.csv", index=False)
rush_ngs.to_csv("misc\\rush_ngs.csv", index=False)
# Add +1 to week for NGS data
rec_ngs["week"] = rec_ngs["week"] + 1
pass_ngs["week"] = pass_ngs["week"] + 1
rush_ngs["week"] = rush_ngs["week"] + 1'''

# Import raw snap count data
snaps = nfl.import_snap_counts(range(first_year,last_year))
print(snaps.head())
snaps.to_csv("misc\\snaps.csv", index=False)

# Import raw win total data
wins = nfl.import_win_totals(range(first_year,last_year))
print(wins.head())
wins.to_csv("misc\\wins.csv", index=False)

# Import raw QBR data
qbr = nfl.import_qbr(range(first_year,last_year))
print(qbr.head())
qbr.to_csv("misc\\qbr.csv", index=False)

# Import raw Score Line data
score_line = nfl.import_sc_lines(range(2018,last_year))
print(score_line.head())
score_line.to_csv("misc\score_line.csv", index=False)

# Import raw PFR data
'''pass_pfr = nfl.import_weekly_pfr("pass", range(2018,last_year))
rush_pfr = nfl.import_weekly_pfr("rush", range(2018,last_year))
rec_pfr = nfl.import_weekly_pfr("rec", range(2018,last_year))
pass_pfr.fillna(-1, inplace=True)
rush_pfr.fillna(-1, inplace=True)
rec_pfr.fillna(-1, inplace=True)
print(pass_pfr.head())
print(rush_pfr.head())
print(rec_pfr.head())
pass_pfr.to_csv("misc\pass_pfr.csv", index=False)
rush_pfr.to_csv("misc\\rush_pfr.csv", index=False)
rec_pfr.to_csv("misc\\rec_pfr.csv", index=False)
print("\nPFR Data Imported!\n")'''

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
print(weekly[0:5]) #Print sample of result
print(weekly.columns) #Print column names
print(weekly["week"].unique()) #Print unique values of "week" column
print("\nWeekly Data Imported!\n") #Print status update

# Function to lookup opposing team given weekly data
def populate_with_opposing_team(row, pbp):
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

def populate_with_snap_counts(row, snaps):
    snap_count = snaps[(snaps['season'] == row['season']) & (snaps['week'] == row['week']) & (snaps['player'] == row['player_display_name'])]
    return snap_count['offense_snaps'].sum()

def populate_with_ngs(row, pass_ngs, rush_ngs, rec_ngs):
    # Subset ngs DataFrames based on 'season' and 'week'
    if row['position'] == 'QB':
        curr_game = pass_ngs[(pass_ngs['season'] == row['season']) & ((pass_ngs['week']) == row['week']) & (pass_ngs['player_display_name'] == row['player_display_name'])]
        if curr_game.empty:
            print(f"NGS QB Empty: {row['player_display_name']} {row['season']} {row['week']}")
            return None
        return curr_game.loc[:,["avg_time_to_throw",
                                  "avg_completed_air_yards",
                                  "avg_intended_air_yards",
                                  "avg_air_yards_differential",
                                  "aggressiveness",
                                  "max_completed_air_distance",
                                  "avg_air_yards_to_sticks",
                                  "passer_rating",
                                  "completion_percentage",
                                  "expected_completion_percentage",
                                  "completion_percentage_above_expectation",
                                  "avg_air_distance",
                                  "max_air_distance"]].reset_index(drop=True).iloc[0]
    elif row['position'] == 'RB':
        curr_game = rush_ngs[(rush_ngs['season'] == row['season']) & ((rush_ngs['week']) == row['week']) & (rush_ngs['player_display_name'] == row['player_display_name'])]
        if curr_game.empty:
            print(f"NGS RB Empty: {row['player_display_name']} {row['season']} {row['week']}")
            return None
        return curr_game.loc[:, ["efficiency",
                                 "percent_attempts_gte_eight_defenders",
                                 "avg_time_to_los",
                                 "rush_attempts",
                                 "rush_yards",
                                 "expected_rush_yards",
                                 "rush_yards_over_expected",
                                 "avg_rush_yards",
                                 "rush_yards_over_expected_per_att",
                                 "rush_pct_over_expected"]].reset_index(drop=True).iloc[0]
    elif row['position'] == 'WR' or row['position'] == 'TE':
        curr_game = rec_ngs[(rec_ngs['season'] == row['season']) & ((rec_ngs['week']) == row['week']) & (rec_ngs['player_display_name'] == row['player_display_name'])]
        if curr_game.empty:
            print(f"NGS WR/TE Empty: {row['player_display_name']} {row['season']} {row['week']}")
            return None
        return curr_game.loc[:, ["avg_cushion",
                                 "avg_separation",
                                 "avg_intended_air_yards",
                                 "percent_share_of_intended_air_yards",
                                 "catch_percentage",
                                 "avg_yac",
                                 "avg_expected_yac",
                                 "avg_yac_above_expectation"]].reset_index(drop=True).iloc[0]
    else:
        return None

def populate_with_pfr(row, pass_pfr, rush_pfr, rec_pfr):
    # Subset pfr DataFrames based on 'season' and 'week'
    if row['position'] == 'QB':
        
        curr_game_pass = pass_pfr[(pass_pfr['season'] == row['season']) & ((pass_pfr['week']) == row['week']) & (pass_pfr['pfr_player_name'] == row['player_display_name'])]
        curr_game_rush = rush_pfr[(rush_pfr['season'] == row['season']) & ((rush_pfr['week']) == row['week']) & (rush_pfr['pfr_player_name'] == row['player_display_name'])]


        if curr_game_pass.empty:
            print(f"PFR QB Empty: {row['player_display_name']} {row['season']} {row['week']}")
            return None
        
        elif curr_game_rush.empty:
            return (curr_game_pass.loc[:,["passing_drops",
                                "passing_drop_pct",
                                "passing_bad_throws",
                                "passing_bad_throw_pct",
                                "times_blitzed",
                                "times_hurried",
                                "times_hit",
                                "times_pressured",
                                "times_pressured_pct"]])
        
        return (curr_game_pass.loc[:,["passing_drops",
                                "passing_drop_pct",
                                "passing_bad_throws",
                                "passing_bad_throw_pct",
                                "times_blitzed",
                                "times_hurried",
                                "times_hit",
                                "times_pressured",
                                "times_pressured_pct"]] + curr_game_rush.loc[:,["rushing_yards_before_contact",
                                                                                     "rushing_yards_before_contact_avg",
                                                                                     "rushing_yards_after_contact",
                                                                                     "rushing_yards_after_contact_avg",
                                                                                     "rushing_broken_tackles"]].reset_index(drop=True).iloc[0])
    
    elif row['position'] == 'RB':
        curr_game_rush = rush_pfr[(rush_pfr['season'] == row['season']) & ((rush_pfr['week']) == row['week']) & (rush_pfr['pfr_player_name'] == row['player_display_name'])]
        curr_game_rec = rec_pfr[(rec_pfr['season'] == row['season']) & ((rec_pfr['week']) == row['week']) & (rec_pfr['pfr_player_name'] == row['player_display_name'])]

        if curr_game_rush.empty:
            print(f"PFR RB Empty: {row['player_display_name']} {row['season']} {row['week']}")
            return None
        
        if curr_game_rec.empty:
            return (curr_game_rush.loc[:, ["rushing_yards_before_contact",
                                 "rushing_yards_before_contact_avg",
                                  "rushing_yards_after_contact",
                                "rushing_yards_after_contact_avg",
                                 "rushing_broken_tackles"]])
        
        return (curr_game_rush.loc[:, ["rushing_yards_before_contact",
                                 "rushing_yards_before_contact_avg",
                                  "rushing_yards_after_contact",
                                "rushing_yards_after_contact_avg",
                                 "rushing_broken_tackles"]] + (curr_game_rec.loc[:,["receiving_broken_tackles",
                                                                                       "passing_drops",
                                                                                       "receiving_drop",
                                                                                       "receiving_drop_pct",
                                                                                       "receiving_int",
                                                                                       "receiving_rat"]]).reset_index(drop=True).iloc[0])
    
    elif row['position'] == 'WR' or row['position'] == 'TE':
        curr_game_rec = rec_pfr[(rec_pfr['season'] == row['season']) & ((rec_pfr['week']) == row['week']) & (rec_pfr['pfr_player_name'] == row['player_display_name'])]
        curr_game_rush = rush_pfr[(rush_pfr['season'] == row['season']) & ((rush_pfr['week']) == row['week']) & (rush_pfr['pfr_player_name'] == row['player_display_name'])]

        if curr_game_rec.empty:
            print(f"PFR WR/TE Empty: {row['player_display_name']} {row['season']} {row['week']}")
            return None
        
        elif curr_game_rush.empty:
            return (curr_game_rec.loc[:, ["receiving_broken_tackles",
                                    "passing_drops",
                                    "receiving_drop",
                                    "receiving_drop_pct",
                                    "receiving_int",
                                    "receiving_rat"]])
        
        return (curr_game_rec.loc[:, ["receiving_broken_tackles",
                                    "passing_drops",
                                    "receiving_drop",
                                    "receiving_drop_pct",
                                    "receiving_int",
                                    "receiving_rat"]] + (curr_game_rush.loc[:,["rushing_yards_before_contact",
                                                                                        "rushing_yards_before_contact_avg",
                                                                                        "rushing_yards_after_contact",
                                                                                        "rushing_yards_after_contact_avg",
                                                                                        "rushing_broken_tackles"]]).reset_index(drop=True).iloc[0])

weekly["opponent_team"] = "null"
weekly["snap_count"] = -1

'''weekly["avg_time_to_throw"] = -1
weekly["avg_completed_air_yards"] = -1
weekly["avg_intended_air_yards"] = -1
weekly["avg_air_yards_differential"] = -1
weekly["aggressiveness"] = -1
weekly["max_completed_air_distance"] = -1
weekly["avg_air_yards_to_sticks"] = -1
weekly["passer_rating"] = -1
weekly["completion_percentage"] = -1
weekly["expected_completion_percentage"] = -1
weekly["completion_percentage_above_expectation"] = -1
weekly["avg_air_distance"] = -1
weekly["max_air_distance"] = -1

weekly["efficiency"] = -1
weekly["percent_attempts_gte_eight_defenders"] = -1
weekly["avg_time_to_los"] = -1
weekly["rush_attempts"] = -1
weekly["rush_yards"] = -1
weekly["expected_rush_yards"] = -1
weekly["rush_yards_over_expected"] = -1
weekly["avg_rush_yards"] = -1
weekly["rush_yards_over_expected_per_att"] = -1
weekly["rush_pct_over_expected"] = -1

weekly["avg_cushion"] = -1
weekly["avg_separation"] = -1
weekly["avg_intended_air_yards"] = -1
weekly["percent_share_of_intended_air_yards"] = -1
weekly["catch_percentage"] = -1
weekly["avg_yac"] = -1
weekly["avg_expected_yac"] = -1
weekly["avg_yac_above_expectation"] = -1

weekly["passing_drops"] = -1
weekly["passing_drop_pct"] = -1
weekly["passing_bad_throws"] = -1
weekly["passing_bad_throw_pct"] = -1
weekly["times_blitzed"] = -1
weekly["times_hurried"] = -1
weekly["times_hit"] = -1
weekly["times_pressured"] = -1
weekly["times_pressured_pct"] = -1

weekly["rushing_yards_before_contact"] = -1
weekly["rushing_yards_before_contact_avg"] = -1
weekly["rushing_yards_after_contact"] = -1
weekly["rushing_yards_after_contact_avg"] = -1
weekly["rushing_broken_tackles"] = -1

weekly["receiving_broken_tackles"] = -1
weekly["receiving_drop"] = -1
weekly["receiving_drop_pct"] = -1
weekly["receiving_int"] = -1
weekly["receiving_rat"] = -1'''

# Access all rows in weekly dataframe using a for loop
for index, row in weekly.iterrows():
    row["opponent_team"] = populate_with_opposing_team(row, pbp)
    row["snap_count"] = populate_with_snap_counts(row, snaps)
    # TODO: CURRENTLY BROKEN. Struggling to debug, might need to reformat into a simpler format similar to opponent_team and snap_count functions

    '''ngs = populate_with_ngs(row, pass_ngs, rush_ngs, rec_ngs)
    if ngs is not None and not ngs.empty:
        for x in ngs.keys():
            row[x] = ngs[x]
    
    pfr = populate_with_pfr(row, pass_pfr, rush_pfr, rec_pfr)
    if pfr is not None and not pfr.empty:
        #print(pfr)
        for x in pfr.keys():
            row[x] = pfr[x]
            #print(row[x])'''

    weekly.loc[index] = row

    print(f"{index}/{len(weekly)}")

# Call function (using TQDM to show progress)
# TODO: FIND WAY TO SPEED UP, its really slow currently, there must be a better way to do it
#tqdm.pandas()
#print("Gathering opponent team data . . .") #Print status update
#weekly['opponent_team'] = weekly.progress_apply(populate_with_opposing_team, args=(pbp,), axis=1)
#print("Gathering snap count data . . .") #Print status update
#weekly['snap_count'] = weekly.progress_apply(populate_with_snap_counts, args=(snaps,), axis=1)

print("Outside Data Compilation Complete! Sample output:\n") #Print status update
print(weekly.head()) #Print sample of result

# Create QB DF
print("QB Data Importing . . .\n") #Print status update
qb = weekly[weekly["position"].isin(["QB"])].reset_index(drop=True) #Create new dataframe for relevant QB information
qb["label"] = qb.progress_apply(lambda row: row["player_id"] + ":" + str(row["season"]) + ":" + str(row["week"]).zfill(2) + ":" + row["recent_team"] + ":" + row["opponent_team"], axis=1)
qb = qb.loc[:, ["player_display_name",
                "label",
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
                "fantasy_points",
                "snap_count"]]
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
                "fantasy_points_ppr",
                "snap_count"]]
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
                "fantasy_points_ppr",
                "snap_count"]]
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
                "fantasy_points_ppr",
                "snap_count"]]
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