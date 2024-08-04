import pandas as pd

game_coverage = 20

te = pd.read_csv('data/te.csv')
te.fillna(-1, inplace=True)
te.sort_values(by=['label'], inplace=True)
te.reset_index(drop=True, inplace=True)

print(te.head())

d = pd.read_csv('data/d.csv')
d = d.iloc[::-1].reset_index(drop=True)

te_nn = pd.DataFrame()

#receptions,targets,receiving_yards,receiving_tds,receiving_fumbles,receiving_air_yards,receiving_yards_after_catch,receiving_first_downs,receiving_epa,receiving_2pt_conversions,racr,target_share,air_yards_share,wopr,special_teams_tds,fantasy_points,fantasy_points_ppr,snap_count

te_nn = pd.concat([te_nn, pd.DataFrame(columns=["receptions",
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
                                                "fantasy_points_ppr_historical",
                                                "snap_count"])])

we_nn = pd.concat([te_nn, pd.DataFrame(columns=["opp_interceptions",
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
                                                "opp_special_teams_tds_allowed"])])

te_nn.insert(0, 'fantasy_points_ppr', 0)
te_nn.insert(0, '2023', False)
te_nn.insert(0, 'id', "")
te_nn.insert(0, 'display_name', "")

te_nn = te_nn.reindex(te.index)

te_nn.sort_index(inplace=True)

prev_id = None
curr_id_count = 0

data_to_drop = []

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
    te_nn.at[i, "display_name"] = data["player_display_name"]
    

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
        data_to_drop.append(i)
    else:
        #print(f"Game {curr_id_count} of career")
        opp_interceptions_count = 0
        opp_sacks_count = 0
        opp_sack_yards_count = 0
        opp_sack_fumbles_count = 0
        opp_sack_fumbles_recovered_count = 0
        opp_receiving_fumbles_count = 0
        opp_receiving_fumbles_recovered_count = 0
        opp_rushing_yards_allowed_count = 0
        opp_passing_yards_allowed_count = 0
        opp_passing_tds_allowed_count = 0
        opp_rushing_tds_allowed_count = 0
        opp_special_teams_tds_allowed_count = 0

        while(d_count!=game_coverage):
            opp_interceptions_count += d_history.iloc[d_loop_idx]["interceptions"]
            opp_sacks_count += d_history.iloc[d_loop_idx]["sacks"]
            opp_sack_yards_count += d_history.iloc[d_loop_idx]["sack_yards"]
            opp_sack_fumbles_count += d_history.iloc[d_loop_idx]["sack_fumbles"]
            opp_sack_fumbles_recovered_count += d_history.iloc[d_loop_idx]["sack_fumbles_recovered"]
            opp_receiving_fumbles_count += d_history.iloc[d_loop_idx]["receiving_fumbles"]
            opp_receiving_fumbles_recovered_count += d_history.iloc[d_loop_idx]["receiving_fumbles_recovered"]
            opp_rushing_yards_allowed_count += d_history.iloc[d_loop_idx]["rushing_yards_allowed"]
            opp_passing_yards_allowed_count += d_history.iloc[d_loop_idx]["passing_yards_allowed"]
            opp_passing_tds_allowed_count += d_history.iloc[d_loop_idx]["passing_tds_allowed"]
            opp_rushing_tds_allowed_count += d_history.iloc[d_loop_idx]["rushing_tds_allowed"]
            opp_special_teams_tds_allowed_count += d_history.iloc[d_loop_idx]["special_teams_tds_allowed"]

            d_loop_idx-=1

            if(d_loop_idx<0):
                d_loop_idx = d_data_idx-1

            d_count+=1

        te_nn.at[i,"opp_interceptions"] = opp_interceptions_count/game_coverage
        te_nn.at[i,"opp_sacks"] = opp_sacks_count/game_coverage
        te_nn.at[i,"opp_sack_yards"] = opp_sack_yards_count/game_coverage
        te_nn.at[i,"opp_sack_fumbles"] = opp_sack_fumbles_count/game_coverage
        te_nn.at[i,"opp_sack_fumbles_recovered"] = opp_sack_fumbles_recovered_count/game_coverage
        te_nn.at[i,"opp_receiving_fumbles"] = opp_receiving_fumbles_count/game_coverage
        te_nn.at[i,"opp_receiving_fumbles_recovered"] = opp_receiving_fumbles_recovered_count/game_coverage
        te_nn.at[i,"opp_rushing_yards_allowed"] = opp_rushing_yards_allowed_count/game_coverage
        te_nn.at[i,"opp_passing_yards_allowed"] = opp_passing_yards_allowed_count/game_coverage
        te_nn.at[i,"opp_passing_tds_allowed"] = opp_passing_tds_allowed_count/game_coverage
        te_nn.at[i,"opp_rushing_tds_allowed"] = opp_rushing_tds_allowed_count/game_coverage
        te_nn.at[i,"opp_special_teams_tds_allowed"] = opp_special_teams_tds_allowed_count/game_coverage     

        receptions_count = 0
        target_count = 0
        receiving_yards_count = 0
        receiving_tds_count = 0
        receiving_fumbles_count = 0
        receiving_air_yards_count = 0
        receiving_yards_after_catch_count = 0
        receiving_first_downs_count = 0
        receiving_epa_count = 0
        receiving_2pt_conversions_count = 0
        racr_count = 0
        target_share_count = 0
        air_yards_share_count = 0
        wopr_count = 0
        special_teams_tds_count = 0
        fantasy_points_ppr_historial_count = 0
        snap_count_count = 0

        while(count!=game_coverage):
            receptions_count += player_history.iloc[loop_idx]["receptions"]
            target_count += player_history.iloc[loop_idx]["targets"]
            receiving_yards_count += player_history.iloc[loop_idx]["receiving_yards"]
            receiving_tds_count += player_history.iloc[loop_idx]["receiving_tds"]
            receiving_fumbles_count += player_history.iloc[loop_idx]["receiving_fumbles"]
            receiving_air_yards_count += player_history.iloc[loop_idx]["receiving_air_yards"]
            receiving_yards_after_catch_count += player_history.iloc[loop_idx]["receiving_yards_after_catch"]
            receiving_first_downs_count += player_history.iloc[loop_idx]["receiving_first_downs"]
            receiving_epa_count += player_history.iloc[loop_idx]["receiving_epa"]
            receiving_2pt_conversions_count += player_history.iloc[loop_idx]["receiving_2pt_conversions"]
            racr_count += player_history.iloc[loop_idx]["racr"]
            target_share_count += player_history.iloc[loop_idx]["target_share"]
            air_yards_share_count += player_history.iloc[loop_idx]["air_yards_share"]
            wopr_count += player_history.iloc[loop_idx]["wopr"]
            special_teams_tds_count += player_history.iloc[loop_idx]["special_teams_tds"]
            fantasy_points_ppr_historial_count += player_history.iloc[loop_idx]["fantasy_points_ppr"]
            snap_count_count += player_history.iloc[loop_idx]["snap_count"]

            loop_idx-=1

            if(loop_idx<0):
                loop_idx = curr_id_count-1

            count+=1
        curr_id_count+=1
    
        te_nn.at[i,"receptions"] = receptions_count/game_coverage
        te_nn.at[i,"targets"] = target_count/game_coverage
        te_nn.at[i,"receiving_yards"] = receiving_yards_count/game_coverage
        te_nn.at[i,"receiving_tds"] = receiving_tds_count/game_coverage
        te_nn.at[i,"receiving_fumbles"] = receiving_fumbles_count/game_coverage
        te_nn.at[i,"receiving_air_yards"] = receiving_air_yards_count/game_coverage
        te_nn.at[i,"receiving_yards_after_catch"] = receiving_yards_after_catch_count/game_coverage
        te_nn.at[i,"receiving_first_downs"] = receiving_first_downs_count/game_coverage
        te_nn.at[i,"receiving_epa"] = receiving_epa_count/game_coverage
        te_nn.at[i,"receiving_2pt_conversions"] = receiving_2pt_conversions_count/game_coverage
        te_nn.at[i,"racr"] = racr_count/game_coverage
        te_nn.at[i,"target_share"] = target_share_count/game_coverage
        te_nn.at[i,"air_yards_share"] = air_yards_share_count/game_coverage
        te_nn.at[i,"wopr"] = wopr_count/game_coverage
        te_nn.at[i,"special_teams_tds"] = special_teams_tds_count/game_coverage
        te_nn.at[i,"fantasy_points_ppr_historical"] = fantasy_points_ppr_historial_count/game_coverage
        te_nn.at[i,"snap_count"] = snap_count_count/game_coverage

    te_nn.at[i,"fantasy_points_ppr"] = data["fantasy_points_ppr"]

te_nn.drop(data_to_drop, inplace=True)
te_nn.reset_index(drop=True, inplace=True)

te_nn.fillna(0, inplace=True)

print(te_nn.head())

te_nn.to_csv('nn_data/te_nn.csv', index=False)