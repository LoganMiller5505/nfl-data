import pandas as pd

game_coverage = 5

qb = pd.read_csv('data/qb.csv')
qb.sort_values(by=['label'], inplace=True)
qb.reset_index(drop=True, inplace=True)

print(qb.head())

d = pd.read_csv('data/d.csv')
d = d.iloc[::-1].reset_index(drop=True)

qb_nn = pd.DataFrame()

for x in range(1,game_coverage+1):
    new_columns = pd.DataFrame(columns=[
                        f"{x}_completions",
                        f"{x}_attempts",
                        f"{x}_passing_yards",
                        f"{x}_passing_tds",
                        f"{x}_interceptions",
                        f"{x}_sacks",
                        f"{x}_sack_fumbles",
                        f"{x}_passing_air_yards",
                        f"{x}_passing_yards_after_catch",
                        f"{x}_passing_first_downs",
                        f"{x}_passing_epa",
                        f"{x}_passing_2pt_conversions",
                        f"{x}_pacr",
                        f"{x}_dakota",
                        f"{x}_carries",
                        f"{x}_rushing_yards",
                        f"{x}_rushing_tds",
                        f"{x}_rushing_fumbles",
                        f"{x}_rushing_first_downs",
                        f"{x}_rushing_epa",
                        f"{x}_rushing_2pt_conversions",
                        f"{x}_fantasy_points",

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
    qb_nn = pd.concat([qb_nn, new_columns])

qb_nn.insert(0, 'fantasy_points', 0)

qb_nn = qb_nn.reindex(qb.index)

qb_nn.sort_index(inplace=True)

prev_id = None
curr_id_count = 0

for i in range(0,len(qb_nn)):

    print(f"{i}/{len(qb_nn)-1}")

    data = qb.iloc[i]

    player_id, season, week, curr_team, curr_def = data["label"].split(':')

    #print(f"Season: {season}, Week: {week}, Player: {player_id}, Team: {curr_team}, Defense: {curr_def}")
    d_history = d.loc[(d['defending_team'] == curr_def)].reset_index(drop=True)
    #print(d_history.head(17))
    d_data = d_history.loc[(d_history['season'] == int(season)) & (d_history['week'] == int(week))]
    #print(d_data)
    d_data_idx = d_data.index[0]
    

    player_history = qb.loc[(player_id == qb['label'].str[:10])].reset_index(drop=True)

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
            qb_nn.at[i,f"{d_count+1}_opp_interceptions"] = d_history.iloc[d_loop_idx]["interceptions"]
            qb_nn.at[i,f"{d_count+1}_opp_sacks"] = d_history.iloc[d_loop_idx]["sacks"]
            qb_nn.at[i,f"{d_count+1}_opp_sack_yards"] = d_history.iloc[d_loop_idx]["sack_yards"]
            qb_nn.at[i,f"{d_count+1}_opp_sack_fumbles"] = d_history.iloc[d_loop_idx]["sack_fumbles"]
            qb_nn.at[i,f"{d_count+1}_opp_sack_fumbles_recovered"] = d_history.iloc[d_loop_idx]["sack_fumbles_recovered"]
            qb_nn.at[i,f"{d_count+1}_opp_receiving_fumbles"] = d_history.iloc[d_loop_idx]["receiving_fumbles"]
            qb_nn.at[i,f"{d_count+1}_opp_receiving_fumbles_recovered"] = d_history.iloc[d_loop_idx]["receiving_fumbles_recovered"]
            qb_nn.at[i,f"{d_count+1}_opp_rushing_yards_allowed"] = d_history.iloc[d_loop_idx]["rushing_yards_allowed"]
            qb_nn.at[i,f"{d_count+1}_opp_passing_yards_allowed"] = d_history.iloc[d_loop_idx]["passing_yards_allowed"]
            qb_nn.at[i,f"{d_count+1}_opp_passing_tds_allowed"] = d_history.iloc[d_loop_idx]["passing_tds_allowed"]
            qb_nn.at[i,f"{d_count+1}_opp_rushing_tds_allowed"] = d_history.iloc[d_loop_idx]["rushing_tds_allowed"]
            qb_nn.at[i,f"{d_count+1}_opp_special_teams_tds_allowed"] = d_history.iloc[d_loop_idx]["special_teams_tds_allowed"]

            d_loop_idx-=1

            if(d_loop_idx<0):
                d_loop_idx = d_data_idx-1
            
            d_count+=1


        while(count!=game_coverage):
            qb_nn.at[i,f"{count+1}_completions"] = player_history.iloc[loop_idx]["completions"]
            qb_nn.at[i,f"{count+1}_attempts"] = player_history.iloc[loop_idx]["attempts"]
            qb_nn.at[i,f"{count+1}_passing_yards"] = player_history.iloc[loop_idx]["passing_yards"]
            qb_nn.at[i,f"{count+1}_passing_tds"] = player_history.iloc[loop_idx]["passing_tds"]
            qb_nn.at[i,f"{count+1}_interceptions"] = player_history.iloc[loop_idx]["interceptions"]
            qb_nn.at[i,f"{count+1}_sacks"] = player_history.iloc[loop_idx]["sacks"]
            qb_nn.at[i,f"{count+1}_sack_fumbles"] = player_history.iloc[loop_idx]["sack_fumbles"]
            qb_nn.at[i,f"{count+1}_passing_air_yards"] = player_history.iloc[loop_idx]["passing_air_yards"]
            qb_nn.at[i,f"{count+1}_passing_yards_after_catch"] = player_history.iloc[loop_idx]["passing_yards_after_catch"]
            qb_nn.at[i,f"{count+1}_passing_first_downs"] = player_history.iloc[loop_idx]["passing_first_downs"]
            qb_nn.at[i,f"{count+1}_passing_epa"] = player_history.iloc[loop_idx]["passing_epa"]
            qb_nn.at[i,f"{count+1}_passing_2pt_conversions"] = player_history.iloc[loop_idx]["passing_2pt_conversions"]
            qb_nn.at[i,f"{count+1}_pacr"] = player_history.iloc[loop_idx]["pacr"]
            qb_nn.at[i,f"{count+1}_dakota"] = player_history.iloc[loop_idx]["dakota"]
            qb_nn.at[i,f"{count+1}_carries"] = player_history.iloc[loop_idx]["carries"]
            qb_nn.at[i,f"{count+1}_rushing_yards"] = player_history.iloc[loop_idx]["rushing_yards"]
            qb_nn.at[i,f"{count+1}_rushing_tds"] = player_history.iloc[loop_idx]["rushing_tds"]
            qb_nn.at[i,f"{count+1}_rushing_fumbles"] = player_history.iloc[loop_idx]["rushing_fumbles"]
            qb_nn.at[i,f"{count+1}_rushing_first_downs"] = player_history.iloc[loop_idx]["rushing_first_downs"]
            qb_nn.at[i,f"{count+1}_rushing_epa"] = player_history.iloc[loop_idx]["rushing_epa"]
            qb_nn.at[i,f"{count+1}_rushing_2pt_conversions"] = player_history.iloc[loop_idx]["rushing_2pt_conversions"]
            qb_nn.at[i,f"{count+1}_fantasy_points"] = player_history.iloc[loop_idx]["fantasy_points"]

            loop_idx-=1

            if(loop_idx<0):
                loop_idx = curr_id_count-1

            count+=1
        curr_id_count+=1
    
    qb_nn.at[i,"fantasy_points"] = data["fantasy_points"]

print(qb_nn.head())

qb_nn.dropna(inplace=True)

qb_nn.to_csv('nn_data/qb_nn.csv', index=False)

'''
qb_nn.at[i,f"{x}_opp_interceptions"] = d_data["interceptions"]
qb_nn.at[i,f"{x}_opp_sacks"] = d_data["sacks"]
qb_nn.at[i,f"{x}_opp_sack_yards"] = d_data["sack_yards"]
qb_nn.at[i,f"{x}_opp_sack_fumbles"] = d_data["sack_fumbles"]
qb_nn.at[i,f"{x}_opp_sack_fumbles_recovered"] = d_data["sack_fumbles_recovered"]
qb_nn.at[i,f"{x}_opp_receiving_fumbles"] = d_data["receiving_fumbles"]
qb_nn.at[i,f"{x}_opp_receiving_fumbles_recovered"] = d_data["receiving_fumbles_recovered"]
qb_nn.at[i,f"{x}_opp_rushing_yards_allowed"] = d_data["rushing_yards_allowed"]
qb_nn.at[i,f"{x}_opp_passing_yards_allowed"] = d_data["passing_yards_allowed"]
qb_nn.at[i,f"{x}_opp_passing_tds_allowed"] = d_data["passing_tds_allowed"]
qb_nn.at[i,f"{x}_opp_rushing_tds_allowed"] = d_data["rushing_tds_allowed"]
qb_nn.at[i,f"{x}_opp_special_teams_tds_allowed"] = d_data["special_teams_tds_allowed"]
'''