from joblib import load
import nfl_data_py as nfl
import pandas as pd

# Load the model
model = load("limited_models/rb_rf.joblib")

# Load the data
rb_nn = pd.read_csv("nn_data/rb_nn.csv")

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

players = players[players["position_group"] == "RB"]
players = players[players["status"] == "ACT"].reset_index(drop=True)
pd.set_option('display.max_columns', None)
print(players.head())

new_nn = pd.DataFrame()
new_nn["display_name"] = ""
new_nn["carries"] = 0
new_nn["rushing_yards"] = 0
new_nn["rushing_tds"] = 0
new_nn["rushing_fumbles"] = 0
new_nn["rushing_first_downs"] = 0
new_nn["rushing_epa"] = 0
new_nn["rushing_2pt_conversions"] = 0
new_nn["receptions"] = 0
new_nn["targets"] = 0
new_nn["receiving_yards"] = 0
new_nn["receiving_tds"] = 0
new_nn["receiving_fumbles"] = 0
new_nn["receiving_air_yards"] = 0
new_nn["receiving_yards_after_catch"] = 0
new_nn["receiving_first_downs"] = 0
new_nn["receiving_epa"] = 0
new_nn["receiving_2pt_conversions"] = 0
new_nn["racr"] = 0
new_nn["target_share"] = 0
new_nn["air_yards_share"] = 0
new_nn["wopr"] = 0
new_nn["special_teams_tds"] = 0
new_nn["fantasy_points_ppr_historical"] = 0
new_nn["snap_count"] = 0


idx_count = 0
for index, row in players.iterrows():

    most_recent_player_data = rb_nn[rb_nn["display_name"] == row["display_name"]]

    if(most_recent_player_data.empty):
        print("No data for player")
        continue

    most_recent_player_data = most_recent_player_data.iloc[-1]

    for i in range(1, 19):
        new_nn.at[idx_count,"display_name"] = row["display_name"]
        new_nn.at[idx_count,"carries"] = most_recent_player_data["carries"]
        new_nn.at[idx_count,"rushing_yards"] = most_recent_player_data["rushing_yards"]
        new_nn.at[idx_count,"rushing_tds"] = most_recent_player_data["rushing_tds"]
        new_nn.at[idx_count,"rushing_fumbles"] = most_recent_player_data["rushing_fumbles"]
        new_nn.at[idx_count,"rushing_first_downs"] = most_recent_player_data["rushing_first_downs"]
        new_nn.at[idx_count,"rushing_epa"] = most_recent_player_data["rushing_epa"]
        new_nn.at[idx_count,"rushing_2pt_conversions"] = most_recent_player_data["rushing_2pt_conversions"]
        new_nn.at[idx_count,"receptions"] = most_recent_player_data["receptions"]
        new_nn.at[idx_count,"targets"] = most_recent_player_data["targets"]
        new_nn.at[idx_count,"receiving_yards"] = most_recent_player_data["receiving_yards"]
        new_nn.at[idx_count,"receiving_tds"] = most_recent_player_data["receiving_tds"]
        new_nn.at[idx_count,"receiving_fumbles"] = most_recent_player_data["receiving_fumbles"]
        new_nn.at[idx_count,"receiving_air_yards"] = most_recent_player_data["receiving_air_yards"]
        new_nn.at[idx_count,"receiving_yards_after_catch"] = most_recent_player_data["receiving_yards_after_catch"]
        new_nn.at[idx_count,"receiving_first_downs"] = most_recent_player_data["receiving_first_downs"]
        new_nn.at[idx_count,"receiving_epa"] = most_recent_player_data["receiving_epa"]
        new_nn.at[idx_count,"receiving_2pt_conversions"] = most_recent_player_data["receiving_2pt_conversions"]
        new_nn.at[idx_count,"racr"] = most_recent_player_data["racr"]
        new_nn.at[idx_count,"target_share"] = most_recent_player_data["target_share"]
        new_nn.at[idx_count,"air_yards_share"] = most_recent_player_data["air_yards_share"]
        new_nn.at[idx_count,"wopr"] = most_recent_player_data["wopr"]
        new_nn.at[idx_count,"special_teams_tds"] = most_recent_player_data["special_teams_tds"]
        new_nn.at[idx_count,"fantasy_points_ppr_historical"] = most_recent_player_data["fantasy_points_ppr_historical"]
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
pd.set_option('display.max_rows', None)
print(predictions)
predictions.to_csv("final_data/rb_final_predictions.csv", index=True)