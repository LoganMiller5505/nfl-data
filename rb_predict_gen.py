import pandas as pd

game_coverage = 5

rb = pd.read_csv('data/rb.csv')
rb = rb[~rb['label'].str.contains('2023')]
rb.sort_values(by=['label'], inplace=True)
rb.reset_index(drop=True, inplace=True)

print(rb.head())

d = pd.read_csv('data/d.csv')
d = d.iloc[::-1].reset_index(drop=True)

rb_nn = pd.DataFrame()

# carries,rushing_yards,rushing_tds,rushing_fumbles,rushing_first_downs,rushing_epa,rushing_2pt_conversions,receptions,targets,receiving_yards,receiving_tds,receiving_fumbles,receiving_air_yards,receiving_yards_after_catch,receiving_first_downs,receiving_epa,receiving_2pt_conversions,racr,target_share,air_yards_share,wopr,special_teams_tds,fantasy_points_ppr

for x in range(1,game_coverage+1):
    new_columns = pd.DataFrame(columns=[
                        f"{x}_carries",
                        f"{x}_rushing_yards",
                        f"{x}_rushing_tds",
                        f"{x}_rushing_fumbles",
                        f"{x}_rushing_first_downs",
                        f"{x}_rushing_epa",
                        f"{x}_rushing_2pt_conversions",
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
    rb_nn = pd.concat([rb_nn, new_columns])

rb_nn.insert(0, 'fantasy_points_ppr', 0)

rb_nn = rb_nn.reindex(rb.index)

rb_nn.sort_index(inplace=True)

prev_id = None
curr_id_count = 0

for i in range(0,len(rb_nn)):

    print(f"{i}/{len(rb_nn)-1}")

    data = rb.iloc[i]

    player_id, season, week, curr_team, curr_def = data["label"].split(':')

    #print(f"Season: {season}, Week: {week}, Player: {player_id}, Team: {curr_team}, Defense: {curr_def}")
    d_history = d.loc[(d['defending_team'] == curr_def)].reset_index(drop=True)
    #print(d_history.head(17))
    d_data = d_history.loc[(d_history['season'] == int(season)) & (d_history['week'] == int(week))]
    #print(d_data)
    d_data_idx = d_data.index[0]
    

    player_history = rb.loc[(player_id == rb['label'].str[:10])].reset_index(drop=True)

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
            rb_nn.at[i,f"{d_count+1}_opp_interceptions"] = d_history.iloc[d_loop_idx]["interceptions"]
            rb_nn.at[i,f"{d_count+1}_opp_sacks"] = d_history.iloc[d_loop_idx]["sacks"]
            rb_nn.at[i,f"{d_count+1}_opp_sack_yards"] = d_history.iloc[d_loop_idx]["sack_yards"]
            rb_nn.at[i,f"{d_count+1}_opp_sack_fumbles"] = d_history.iloc[d_loop_idx]["sack_fumbles"]
            rb_nn.at[i,f"{d_count+1}_opp_sack_fumbles_recovered"] = d_history.iloc[d_loop_idx]["sack_fumbles_recovered"]
            rb_nn.at[i,f"{d_count+1}_opp_receiving_fumbles"] = d_history.iloc[d_loop_idx]["receiving_fumbles"]
            rb_nn.at[i,f"{d_count+1}_opp_receiving_fumbles_recovered"] = d_history.iloc[d_loop_idx]["receiving_fumbles_recovered"]
            rb_nn.at[i,f"{d_count+1}_opp_rushing_yards_allowed"] = d_history.iloc[d_loop_idx]["rushing_yards_allowed"]
            rb_nn.at[i,f"{d_count+1}_opp_passing_yards_allowed"] = d_history.iloc[d_loop_idx]["passing_yards_allowed"]
            rb_nn.at[i,f"{d_count+1}_opp_passing_tds_allowed"] = d_history.iloc[d_loop_idx]["passing_tds_allowed"]
            rb_nn.at[i,f"{d_count+1}_opp_rushing_tds_allowed"] = d_history.iloc[d_loop_idx]["rushing_tds_allowed"]
            rb_nn.at[i,f"{d_count+1}_opp_special_teams_tds_allowed"] = d_history.iloc[d_loop_idx]["special_teams_tds_allowed"]

            d_loop_idx-=1

            if(d_loop_idx<0):
                d_loop_idx = d_data_idx-1
            
            d_count+=1


        while(count!=game_coverage):
            rb_nn.at[i,f"{count+1}_carries"] = player_history.iloc[loop_idx]["carries"]
            rb_nn.at[i,f"{count+1}_rushing_yards"] = player_history.iloc[loop_idx]["rushing_yards"]
            rb_nn.at[i,f"{count+1}_rushing_tds"] = player_history.iloc[loop_idx]["rushing_tds"]
            rb_nn.at[i,f"{count+1}_rushing_fumbles"] = player_history.iloc[loop_idx]["rushing_fumbles"]
            rb_nn.at[i,f"{count+1}_rushing_first_downs"] = player_history.iloc[loop_idx]["rushing_first_downs"]
            rb_nn.at[i,f"{count+1}_rushing_epa"] = player_history.iloc[loop_idx]["rushing_epa"]
            rb_nn.at[i,f"{count+1}_rushing_2pt_conversions"] = player_history.iloc[loop_idx]["rushing_2pt_conversions"]
            rb_nn.at[i,f"{count+1}_receptions"] = player_history.iloc[loop_idx]["receptions"]
            rb_nn.at[i,f"{count+1}_targets"] = player_history.iloc[loop_idx]["targets"]
            rb_nn.at[i,f"{count+1}_receiving_yards"] = player_history.iloc[loop_idx]["receiving_yards"]
            rb_nn.at[i,f"{count+1}_receiving_tds"] = player_history.iloc[loop_idx]["receiving_tds"]
            rb_nn.at[i,f"{count+1}_receiving_fumbles"] = player_history.iloc[loop_idx]["receiving_fumbles"]
            rb_nn.at[i,f"{count+1}_receiving_air_yards"] = player_history.iloc[loop_idx]["receiving_air_yards"]
            rb_nn.at[i,f"{count+1}_receiving_yards_after_catch"] = player_history.iloc[loop_idx]["receiving_yards_after_catch"]
            rb_nn.at[i,f"{count+1}_receiving_first_downs"] = player_history.iloc[loop_idx]["receiving_first_downs"]
            rb_nn.at[i,f"{count+1}_receiving_epa"] = player_history.iloc[loop_idx]["receiving_epa"]
            rb_nn.at[i,f"{count+1}_receiving_2pt_conversions"] = player_history.iloc[loop_idx]["receiving_2pt_conversions"]
            rb_nn.at[i,f"{count+1}_racr"] = player_history.iloc[loop_idx]["racr"]
            rb_nn.at[i,f"{count+1}_target_share"] = player_history.iloc[loop_idx]["target_share"]
            rb_nn.at[i,f"{count+1}_air_yards_share"] = player_history.iloc[loop_idx]["air_yards_share"]
            rb_nn.at[i,f"{count+1}_wopr"] = player_history.iloc[loop_idx]["wopr"]
            rb_nn.at[i,f"{count+1}_special_teams_tds"] = player_history.iloc[loop_idx]["special_teams_tds"]
            rb_nn.at[i,f"{count+1}_fantasy_points_ppr"] = player_history.iloc[loop_idx]["fantasy_points_ppr"]

            loop_idx-=1

            if(loop_idx<0):
                loop_idx = curr_id_count-1

            count+=1
        curr_id_count+=1
    
    rb_nn.at[i,"fantasy_points_ppr"] = data["fantasy_points_ppr"]

print(rb_nn.head())

rb_nn.dropna(inplace=True)

rb_nn.to_csv('limited_nn_data/rb_nn.csv', index=False)