from joblib import load
import nfl_data_py as nfl
import pandas as pd

# Load the model
model = load("limited_models/qb_rf.joblib")

# Load the data
qb_nn = pd.read_csv("nn_data/qb_nn.csv")

d = pd.read_csv("data/d.csv")

players = nfl.import_players()
schedule = nfl.import_schedules([2024]).reset_index(drop=True)

print("Players")
print(players.head())

print("Schedule")
print(schedule.head())

print("Players Info")
print(players.info())
print(players.columns)
print(players["position_group"].unique())
# WR, TE, RB, QB

players = players[players["position_group"] == "QB"]
players = players[players["status"] == "ACT"].reset_index(drop=True)
pd.set_option('display.max_columns', None)
print(players.head())

# "team_abbr"

'''
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
"fantasy_points_historical"
'''

'''
"opp_interceptions",
"opp_sacks",
"opp_sack_yards",
"opp_sack_fumbles",
"opp_sack_fumbles_recovered",
"opp_receiving_fumbles",
"opp_receiving_fumbles_recovered",
"opp_rushing_yards_allowed",
"opp_passing_yards_allowed",
"opp_passing_tds_allowed",
"opp_rushing_tds_allowed",
"opp_special_teams_tds_allowed"
'''

new_nn = pd.DataFrame()
new_nn["display_name"] = ""
new_nn["completions"] = 0
new_nn["attempts"] = 0
new_nn["passing_yards"] = 0
new_nn["passing_tds"] = 0
new_nn["interceptions"] = 0
new_nn["sacks"] = 0
new_nn["sack_fumbles"] = 0
new_nn["passing_air_yards"] = 0
new_nn["passing_yards_after_catch"] = 0
new_nn["passing_first_downs"] = 0
new_nn["passing_epa"] = 0
new_nn["passing_2pt_conversions"] = 0
new_nn["pacr"] = 0
new_nn["dakota"] = 0
new_nn["carries"] = 0
new_nn["rushing_yards"] = 0
new_nn["rushing_tds"] = 0
new_nn["rushing_fumbles"] = 0
new_nn["rushing_first_downs"] = 0
new_nn["rushing_epa"] = 0
new_nn["rushing_2pt_conversions"] = 0
new_nn["fantasy_points_historical"] = 0
new_nn["snap_count"] = 0


idx_count = 0
for index, row in players.iterrows():

    most_recent_player_data = qb_nn[qb_nn["display_name"] == row["display_name"]]

    if(most_recent_player_data.empty):
        print("No data for player")
        continue

    most_recent_player_data = most_recent_player_data.iloc[-1]

    for i in range(1, 19):
        new_nn.at[idx_count,"display_name"] = row["display_name"]
        new_nn.at[idx_count,"completions"] = most_recent_player_data["completions"]
        new_nn.at[idx_count,"attempts"] = most_recent_player_data["attempts"]
        new_nn.at[idx_count,"passing_yards"] = most_recent_player_data["passing_yards"]
        new_nn.at[idx_count,"passing_tds"] = most_recent_player_data["passing_tds"]
        new_nn.at[idx_count,"interceptions"] = most_recent_player_data["interceptions"]
        new_nn.at[idx_count,"sacks"] = most_recent_player_data["sacks"]
        new_nn.at[idx_count,"sack_fumbles"] = most_recent_player_data["sack_fumbles"]
        new_nn.at[idx_count,"passing_air_yards"] = most_recent_player_data["passing_air_yards"]
        new_nn.at[idx_count,"passing_yards_after_catch"] = most_recent_player_data["passing_yards_after_catch"]
        new_nn.at[idx_count,"passing_first_downs"] = most_recent_player_data["passing_first_downs"]
        new_nn.at[idx_count,"passing_epa"] = most_recent_player_data["passing_epa"]
        new_nn.at[idx_count,"passing_2pt_conversions"] = most_recent_player_data["passing_2pt_conversions"]
        new_nn.at[idx_count,"pacr"] = most_recent_player_data["pacr"]
        new_nn.at[idx_count,"dakota"] = most_recent_player_data["dakota"]
        new_nn.at[idx_count,"carries"] = most_recent_player_data["carries"]
        new_nn.at[idx_count,"rushing_yards"] = most_recent_player_data["rushing_yards"]
        new_nn.at[idx_count,"rushing_tds"] = most_recent_player_data["rushing_tds"]
        new_nn.at[idx_count,"rushing_fumbles"] = most_recent_player_data["rushing_fumbles"]
        new_nn.at[idx_count,"rushing_first_downs"] = most_recent_player_data["rushing_first_downs"]
        new_nn.at[idx_count,"rushing_epa"] = most_recent_player_data["rushing_epa"]
        new_nn.at[idx_count,"rushing_2pt_conversions"] = most_recent_player_data["rushing_2pt_conversions"]
        new_nn.at[idx_count,"fantasy_points_historical"] = most_recent_player_data["fantasy_points_historical"]
        new_nn.at[idx_count,"snap_count"] = most_recent_player_data["snap_count"]

        # Get the game where away_team or home_team is the team_abbr and week is i
        print("Week: " + str(i))
        print("Team: " + row["team_abbr"])
        curr_game_away = schedule[(schedule["away_team"] == row["team_abbr"]) & (schedule["week"] == i)]
        curr_game_home = schedule[(schedule["home_team"] == row["team_abbr"]) & (schedule["week"] == i)]
        if(curr_game_away.empty and curr_game_home.empty):
            print("No game for player (bye week)")
            continue
        curr_game = curr_game_away if curr_game_home.empty else curr_game_home
        opp_team = curr_game["away_team"].values[0] if curr_game_away.empty else curr_game["home_team"].values[0]
        print("Opp Team: " + opp_team)
        opp_team_data = d[d["defending_team"] == opp_team].iloc[-1]

        new_nn.at[idx_count,"opp_interceptions"] = opp_team_data["interceptions"]
        new_nn.at[idx_count,"opp_sacks"] = opp_team_data["sacks"]
        new_nn.at[idx_count,"opp_sack_yards"] = opp_team_data["sack_yards"]
        new_nn.at[idx_count,"opp_sack_fumbles"] = opp_team_data["sack_fumbles"]
        new_nn.at[idx_count,"opp_sack_fumbles_recovered"] = opp_team_data["sack_fumbles_recovered"]
        new_nn.at[idx_count,"opp_receiving_fumbles"] = opp_team_data["receiving_fumbles"]
        new_nn.at[idx_count,"opp_receiving_fumbles_recovered"] = opp_team_data["receiving_fumbles_recovered"]
        new_nn.at[idx_count,"opp_rushing_yards_allowed"] = opp_team_data["rushing_yards_allowed"]
        new_nn.at[idx_count,"opp_passing_yards_allowed"] = opp_team_data["passing_yards_allowed"]
        new_nn.at[idx_count,"opp_passing_tds_allowed"] = opp_team_data["passing_tds_allowed"]
        new_nn.at[idx_count,"opp_rushing_tds_allowed"] = opp_team_data["rushing_tds_allowed"]
        new_nn.at[idx_count,"opp_special_teams_tds_allowed"] = opp_team_data["special_teams_tds_allowed"]

        idx_count += 1


print(new_nn.head(18))

name = new_nn["display_name"]

new_nn = new_nn.drop(columns=["display_name"])
new_nn = new_nn.fillna(0)
new_nn = new_nn.astype('float')

predictions = model.predict(new_nn)

print(predictions)

# Save and print the predictions
predictions = pd.DataFrame(predictions)
predictions["fantasy_points"] = predictions
predictions["display_name"] = name
predictions = predictions.groupby("display_name").mean()
predictions = predictions.sort_values(by="fantasy_points", ascending=False)
predictions = predictions.drop(columns=[0])
predictions["position"] = "QB"
pd.set_option('display.max_rows', None)
print(predictions)
predictions.to_csv("final_data/qb_final_predictions.csv", index=True)

# ESPN RANKINGS
'''Josh Allen - 23.5
Jalen Hurts - 21.4
Lamar Jackson - 20.3
Patrick Mahomes - 19.6
C.J. Stroud - 18.9
Anthony Richardson - 18.9
Joe Burrow - 18.7
Jordan Love - 18.1
Caleb Williams - 17.8
Jayden Daniels - 17.7
Baker Mayfield - 17.3
Kyler Murray - 17.2
Daniel Jones - 17.2
Geno Smith - 17.2
Justin Herbert - 17.0
Jared Goff - 16.8
Brock Purdy - 16.6
Deshaun Watson - 16.4
Dak Prescott - 16.3
Aaron Rodgers - 16.2
Matthew Stafford - 16.1
Sam Darnold - 16.0
Russell Wilson - 15.8
Trevor Lawrence - 15.6
Kirk Cousins - 15.6
Tua Tagovailoa - 15.4
Derek Carr - 15.0
Gardner Minshew - 15.0
Will Levis - 14.3
Jacoby Brissett - 13.7
Bryce Young - 13.6
Bo Nix - 13.5'''

# Compare the predictions to the ESPN rankings
espn_rankings = pd.DataFrame()
espn_rankings["display_name"] = ["Josh Allen","Jalen Hurts","Lamar Jackson","Patrick Mahomes","C.J. Stroud","Anthony Richardson","Joe Burrow","Jordan Love","Caleb Williams","Jayden Daniels","Baker Mayfield","Kyler Murray","Daniel Jones","Geno Smith","Justin Herbert","Jared Goff","Brock Purdy","Deshaun Watson","Dak Prescott","Aaron Rodgers","Matthew Stafford","Sam Darnold","Russell Wilson","Trevor Lawrence","Kirk Cousins","Tua Tagovailoa","Derek Carr","Gardner Minshew","Will Levis","Jacoby Brissett","Bryce Young","Bo Nix"]
espn_rankings["fantasy_points"] = [23.5,21.4,20.3,19.6,18.9,18.9,18.7,18.1,17.8,17.7,17.3,17.2,17.2,17.2,17.0,16.8,16.6,16.4,16.3,16.2,16.1,16.0,15.8,15.6,15.6,15.4,15.0,15.0,14.3,13.7,13.6,13.5]
espn_rankings = espn_rankings.set_index("display_name")
print(espn_rankings)

final_predictions = pd.read_csv("final_data/qb_final_predictions.csv")
final_predictions = final_predictions.set_index("display_name")
print(final_predictions)

for index, row in final_predictions.iterrows():
    if index not in espn_rankings.index:
        continue
    print(index)
    print("ESPN: " + str(espn_rankings.loc[index]["fantasy_points"]))
    print("Predicted: " + str(row["fantasy_points"]))
    print("Difference: " + str(espn_rankings.loc[index]["fantasy_points"] - row["fantasy_points"]))
    print("")