import pandas as pd

game_coverage = 10

te = pd.read_csv('data/te.csv')
te.sort_values(by=['label'], inplace=True)
te.reset_index(drop=True, inplace=True)

print(te.head())

d = pd.read_csv('data/d.csv')
d = d.iloc[::-1].reset_index(drop=True)

te_nn = pd.DataFrame()

#receptions,targets,receiving_yards,receiving_tds,receiving_fumbles,receiving_air_yards,receiving_yards_after_catch,receiving_first_downs,receiving_epa,receiving_2pt_conversions,racr,target_share,air_yards_share,wopr,special_teams_tds,fantasy_points,fantasy_points_ppr


for x in range(1,game_coverage+1):
    new_columns = pd.DataFrame(columns=[
                        f"{x}_receptions",
                        f"{x}_targets",
                        f"{x}_receiving_yards",
                        f"{x}_receiving_tds",
                        f"{x}_receiving_fumbles",
                        f"{x}_receiving_air_yards",
                        f"{x}_receiving_yards_after_catch",
                        f"{x}_receiving_first_downs",
                        f"{x}_receiving_epa",
                        f"{x}_receiving_2pt_conversions",
                        f"{x}_racr",
                        f"{x}_target_share",
                        f"{x}_air_yards_share",
                        f"{x}_wopr",
                        f"{x}_special_teams_tds",
                        f"{x}_fantasy_points_ppr",

                        f"{x}_opp_interceptions",
                        f"{x}_opp_sacks",
                        f"{x}_opp_sack_yards",
                        f"{x}_opp_sack_fumbles",
                        f"{x}_opp_sack_fumbles_recovered",
                        f"{x}_opp_receiving_fumbles",
                        f"{x}_opp_receiving_fumbles_recovered",
                        f"{x}_opp_rushing_yards_allowed",
                        f"{x}_opp_passing_yards_allowed",
                        f"{x}_opp_passing_tds_allowed",
                        f"{x}_opp_rushing_tds_allowed",
                        f"{x}_opp_special_teams_tds_allowed"])
    te_nn = pd.concat([te_nn, new_columns])

te_nn.insert(0, 'fantasy_points_ppr', 0)
te_nn.insert(0, '2023', False)
te_nn.insert(0, 'id', "")

te_nn = te_nn.reindex(te.index)

te_nn.sort_index(inplace=True)

prev_id = None
curr_id_count = 0

for i in range(0,len(te_nn)):

    print(f"{i}/{len(te_nn)-1}")

    data = te.iloc[i]

    player_id, season, week, curr_team, curr_def = data["label"].split(':')

    #print(f"Season: {season}, Week: {week}, Player: {player_id}, Team: {curr_team}, Defense: {curr_def}")
    d_history = d.loc[(d['defending_team'] == curr_def)].reset_index(drop=True)
    #print(d_history.head(17))
    d_data = d_history.loc[(d_history['season'] == int(season)) & (d_history['week'] == int(week))]
    #print(d_data)
    d_data_idx = d_data.index[0]
    
    te_nn.at[i, "2023"] = season == "2023"
    te_nn.at[i, "id"] = player_id

    player_history = te.loc[(player_id == te['label'].str[:10])].reset_index(drop=True)

    #print(player_history)

    if(prev_id != player_id):
        prev_id = player_id
        curr_id_count = 0

    loop_idx = curr_id_count-1
    d_loop_idx = d_data_idx-1

    count = 0
    d_count = 0
    
    if(curr_id_count == 0):
        #print("First logged game of career")
        curr_id_count+=1
    else:
        #print(f"Game {curr_id_count} of career")
        while(d_count!=game_coverage):
            te_nn.at[i,f"{d_count+1}_opp_interceptions"] = d_history.iloc[d_loop_idx]["interceptions"]
            te_nn.at[i,f"{d_count+1}_opp_sacks"] = d_history.iloc[d_loop_idx]["sacks"]
            te_nn.at[i,f"{d_count+1}_opp_sack_yards"] = d_history.iloc[d_loop_idx]["sack_yards"]
            te_nn.at[i,f"{d_count+1}_opp_sack_fumbles"] = d_history.iloc[d_loop_idx]["sack_fumbles"]
            te_nn.at[i,f"{d_count+1}_opp_sack_fumbles_recovered"] = d_history.iloc[d_loop_idx]["sack_fumbles_recovered"]
            te_nn.at[i,f"{d_count+1}_opp_receiving_fumbles"] = d_history.iloc[d_loop_idx]["receiving_fumbles"]
            te_nn.at[i,f"{d_count+1}_opp_receiving_fumbles_recovered"] = d_history.iloc[d_loop_idx]["receiving_fumbles_recovered"]
            te_nn.at[i,f"{d_count+1}_opp_rushing_yards_allowed"] = d_history.iloc[d_loop_idx]["rushing_yards_allowed"]
            te_nn.at[i,f"{d_count+1}_opp_passing_yards_allowed"] = d_history.iloc[d_loop_idx]["passing_yards_allowed"]
            te_nn.at[i,f"{d_count+1}_opp_passing_tds_allowed"] = d_history.iloc[d_loop_idx]["passing_tds_allowed"]
            te_nn.at[i,f"{d_count+1}_opp_rushing_tds_allowed"] = d_history.iloc[d_loop_idx]["rushing_tds_allowed"]
            te_nn.at[i,f"{d_count+1}_opp_special_teams_tds_allowed"] = d_history.iloc[d_loop_idx]["special_teams_tds_allowed"]

            d_loop_idx-=1

            if(d_loop_idx<0):
                d_loop_idx = d_data_idx-1
            
            d_count+=1


        while(count!=game_coverage):
            te_nn.at[i,f"{count+1}_receptions"] = player_history.iloc[loop_idx]["receptions"]
            te_nn.at[i,f"{count+1}_targets"] = player_history.iloc[loop_idx]["targets"]
            te_nn.at[i,f"{count+1}_receiving_yards"] = player_history.iloc[loop_idx]["receiving_yards"]
            te_nn.at[i,f"{count+1}_receiving_tds"] = player_history.iloc[loop_idx]["receiving_tds"]
            te_nn.at[i,f"{count+1}_receiving_fumbles"] = player_history.iloc[loop_idx]["receiving_fumbles"]
            te_nn.at[i,f"{count+1}_receiving_air_yards"] = player_history.iloc[loop_idx]["receiving_air_yards"]
            te_nn.at[i,f"{count+1}_receiving_yards_after_catch"] = player_history.iloc[loop_idx]["receiving_yards_after_catch"]
            te_nn.at[i,f"{count+1}_receiving_first_downs"] = player_history.iloc[loop_idx]["receiving_first_downs"]
            te_nn.at[i,f"{count+1}_receiving_epa"] = player_history.iloc[loop_idx]["receiving_epa"]
            te_nn.at[i,f"{count+1}_receiving_2pt_conversions"] = player_history.iloc[loop_idx]["receiving_2pt_conversions"]
            te_nn.at[i,f"{count+1}_racr"] = player_history.iloc[loop_idx]["racr"]
            te_nn.at[i,f"{count+1}_target_share"] = player_history.iloc[loop_idx]["target_share"]
            te_nn.at[i,f"{count+1}_air_yards_share"] = player_history.iloc[loop_idx]["air_yards_share"]
            te_nn.at[i,f"{count+1}_wopr"] = player_history.iloc[loop_idx]["wopr"]
            te_nn.at[i,f"{count+1}_special_teams_tds"] = player_history.iloc[loop_idx]["special_teams_tds"]
            te_nn.at[i,f"{count+1}_fantasy_points_ppr"] = player_history.iloc[loop_idx]["fantasy_points_ppr"]

            loop_idx-=1

            if(loop_idx<0):
                loop_idx = curr_id_count-1

            count+=1
        curr_id_count+=1
    
    te_nn.at[i,"fantasy_points_ppr"] = data["fantasy_points_ppr"]

te_nn.fillna(0, inplace=True)

print(te_nn.head())

te_nn.to_csv('nn_data/te_nn.csv', index=False)