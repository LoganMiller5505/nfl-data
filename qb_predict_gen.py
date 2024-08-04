import pandas as pd

game_coverage = 20

qb = pd.read_csv('data/qb.csv')
qb.fillna(-1, inplace=True)
'''for index, row in qb.iterrows():
    print(row)'''
qb.sort_values(by=['label'], inplace=True)
# Exclude entries where "avg_time_to_throw","avg_completed_air_yards","avg_intended_air_yards","avg_air_yards_differential","aggressiveness","max_completed_air_distance","avg_air_yards_to_sticks","passer_rating","completion_percentage","expected_completion_percentage","completion_percentage_above_expectation","avg_air_distance", and "max_air_distance" are all -1
#qb = qb.loc[(qb['avg_time_to_throw'] != -1) & (qb['avg_completed_air_yards'] != -1) & (qb['avg_intended_air_yards'] != -1) & (qb['avg_air_yards_differential'] != -1) & (qb['aggressiveness'] != -1) & (qb['max_completed_air_distance'] != -1) & (qb['avg_air_yards_to_sticks'] != -1) & (qb['passer_rating'] != -1) & (qb['completion_percentage'] != -1) & (qb['expected_completion_percentage'] != -1) & (qb['completion_percentage_above_expectation'] != -1) & (qb['avg_air_distance'] != -1) & (qb['max_air_distance'] != -1)]
# Exclude entires where passing_drops, passing_drop_pct, passing_bad_throws, passing_bad_throw_pct, times_blitzed, times_hurried, times_hit,times_pressured, and times_pressured_pct are all 0
#qb = qb.loc[(qb['passing_drops'] != -1) & (qb['passing_drop_pct'] != -1) & (qb['passing_bad_throws'] != -1) & (qb['passing_bad_throw_pct'] != -1) & (qb['times_blitzed'] != -1) & (qb['times_hurried'] != -1) & (qb['times_hit'] != -1) & (qb['times_pressured'] != -1) & (qb['times_pressured_pct'] != -1)]

qb.reset_index(drop=True, inplace=True)

print(qb.head())
#print(qb["avg_time_to_throw"].head())
#print(qb["passing_drops"].head())

d = pd.read_csv('data/d.csv')
d = d.iloc[::-1].reset_index(drop=True)

qb_nn = pd.DataFrame()

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
"fantasy_points",
"snap_count",
"avg_time_to_throw",
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
"max_air_distance",
"passing_drops",
"passing_drop_pct",
"passing_bad_throws",
"passing_bad_throw_pct",
"times_blitzed",
"times_hurried",
"times_hit",
"times_pressured",
"times_pressured_pct",
"rushing_yards_before_contact",
"rushing_yards_before_contact_avg",
"rushing_yards_after_contact",
"rushing_yards_after_contact_avg",
"rushing_broken_tackles",
'''

qb_nn = pd.concat([qb_nn, pd.DataFrame(columns=["completions",
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
                                                "fantasy_points_historical",
                                                "snap_count"])])

qb_nn = pd.concat([qb_nn, pd.DataFrame(columns=["opp_interceptions",
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

qb_nn.insert(0, 'fantasy_points', 0)
qb_nn.insert(0, '2023', False)
qb_nn.insert(0, 'id', "")
qb_nn.insert(0, 'display_name', "")

qb_nn = qb_nn.reindex(qb.index)

qb_nn.sort_index(inplace=True)

prev_id = None
curr_id_count = 0

data_to_drop = []

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
    
    qb_nn.at[i, "2023"] = season == "2023"
    qb_nn.at[i, "id"] = player_id
    qb_nn.at[i, "display_name"] = data["player_display_name"]

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
        
        qb_nn.at[i,"opp_interceptions"] = opp_interceptions_count/game_coverage
        qb_nn.at[i,"opp_sacks"] = opp_sacks_count/game_coverage
        qb_nn.at[i,"opp_sack_yards"] = opp_sack_yards_count/game_coverage
        qb_nn.at[i,"opp_sack_fumbles"] = opp_sack_fumbles_count/game_coverage
        qb_nn.at[i,"opp_sack_fumbles_recovered"] = opp_sack_fumbles_recovered_count/game_coverage
        qb_nn.at[i,"opp_receiving_fumbles"] = opp_receiving_fumbles_count/game_coverage
        qb_nn.at[i,"opp_receiving_fumbles_recovered"] = opp_receiving_fumbles_recovered_count/game_coverage
        qb_nn.at[i,"opp_rushing_yards_allowed"] = opp_rushing_yards_allowed_count/game_coverage
        qb_nn.at[i,"opp_passing_yards_allowed"] = opp_passing_yards_allowed_count/game_coverage
        qb_nn.at[i,"opp_passing_tds_allowed"] = opp_passing_tds_allowed_count/game_coverage
        qb_nn.at[i,"opp_rushing_tds_allowed"] = opp_rushing_tds_allowed_count/game_coverage
        qb_nn.at[i,"opp_special_teams_tds_allowed"] = opp_special_teams_tds_allowed_count/game_coverage

        completions_count = 0
        attempts_count = 0
        passing_yards_count = 0
        passing_tds_count = 0
        interceptions_count = 0
        sacks_count = 0
        sack_fumbles_count = 0
        passing_air_yards_count = 0
        passing_yards_after_catch_count = 0
        passing_first_downs_count = 0
        passing_epa_count = 0
        passing_2pt_conversions_count = 0
        pacr_count = 0
        dakota_count = 0
        carries_count = 0
        rushing_yards_count = 0
        rushing_tds_count = 0
        rushing_fumbles_count = 0
        rushing_first_downs_count = 0
        rushing_epa_count = 0
        rushing_2pt_conversions_count = 0
        fantasy_points_historical_count = 0

        snap_count_count = 0

        '''avg_time_to_throw_count = 0
        avg_completed_air_yards_count = 0
        avg_intended_air_yards_count = 0
        avg_air_yards_differential_count = 0
        aggressiveness_count = 0
        max_completed_air_distance_count = 0
        avg_air_yards_to_sticks_count = 0
        passer_rating_count = 0
        completion_percentage_count = 0
        expected_completion_percentage_count = 0
        completion_percentage_above_expectation_count = 0
        avg_air_distance_count = 0
        max_air_distance_count = 0

        passing_drops_count = 0
        passing_drop_pct_count = 0
        passing_bad_throws_count = 0
        passing_bad_throw_pct_count = 0
        times_blitzed_count = 0
        times_hurried_count = 0
        times_hit_count = 0
        times_pressured_count = 0
        times_pressured_pct_count = 0
        rushing_yards_before_contact_count = 0
        rushing_yards_before_contact_avg_count = 0
        rushing_yards_after_contact_count = 0
        rushing_yards_after_contact_avg_count = 0
        rushing_broken_tackles_count = 0'''

        while(count!=game_coverage):
            completions_count += player_history.iloc[loop_idx]["completions"]
            attempts_count += player_history.iloc[loop_idx]["attempts"]
            passing_yards_count += player_history.iloc[loop_idx]["passing_yards"]
            passing_tds_count += player_history.iloc[loop_idx]["passing_tds"]
            interceptions_count += player_history.iloc[loop_idx]["interceptions"]
            sacks_count += player_history.iloc[loop_idx]["sacks"]
            sack_fumbles_count += player_history.iloc[loop_idx]["sack_fumbles"]
            passing_air_yards_count += player_history.iloc[loop_idx]["passing_air_yards"]
            passing_yards_after_catch_count += player_history.iloc[loop_idx]["passing_yards_after_catch"]
            passing_first_downs_count += player_history.iloc[loop_idx]["passing_first_downs"]
            passing_epa_count += player_history.iloc[loop_idx]["passing_epa"]
            passing_2pt_conversions_count += player_history.iloc[loop_idx]["passing_2pt_conversions"]
            pacr_count += player_history.iloc[loop_idx]["pacr"]
            dakota_count += player_history.iloc[loop_idx]["dakota"]
            carries_count += player_history.iloc[loop_idx]["carries"]
            rushing_yards_count += player_history.iloc[loop_idx]["rushing_yards"]
            rushing_tds_count += player_history.iloc[loop_idx]["rushing_tds"]
            rushing_fumbles_count += player_history.iloc[loop_idx]["rushing_fumbles"]
            rushing_first_downs_count += player_history.iloc[loop_idx]["rushing_first_downs"]
            rushing_epa_count += player_history.iloc[loop_idx]["rushing_epa"]
            rushing_2pt_conversions_count += player_history.iloc[loop_idx]["rushing_2pt_conversions"]
            fantasy_points_historical_count += player_history.iloc[loop_idx]["fantasy_points"]

            snap_count_count += player_history.iloc[loop_idx]["snap_count"]

            '''avg_time_to_throw_count += player_history.iloc[loop_idx]["avg_time_to_throw"]
            avg_completed_air_yards_count += player_history.iloc[loop_idx]["avg_completed_air_yards"]
            avg_intended_air_yards_count += player_history.iloc[loop_idx]["avg_intended_air_yards"]
            avg_air_yards_differential_count += player_history.iloc[loop_idx]["avg_air_yards_differential"]
            aggressiveness_count += player_history.iloc[loop_idx]["aggressiveness"]
            max_completed_air_distance_count += player_history.iloc[loop_idx]["max_completed_air_distance"]
            avg_air_yards_to_sticks_count += player_history.iloc[loop_idx]["avg_air_yards_to_sticks"]
            passer_rating_count += player_history.iloc[loop_idx]["passer_rating"]
            completion_percentage_count += player_history.iloc[loop_idx]["completion_percentage"]
            expected_completion_percentage_count += player_history.iloc[loop_idx]["expected_completion_percentage"]
            completion_percentage_above_expectation_count += player_history.iloc[loop_idx]["completion_percentage_above_expectation"]
            avg_air_distance_count += player_history.iloc[loop_idx]["avg_air_distance"]
            max_air_distance_count += player_history.iloc[loop_idx]["max_air_distance"]

            passing_drops_count += player_history.iloc[loop_idx]["passing_drops"]
            passing_drop_pct_count += player_history.iloc[loop_idx]["passing_drop_pct"]
            passing_bad_throws_count += player_history.iloc[loop_idx]["passing_bad_throws"]
            passing_bad_throw_pct_count += player_history.iloc[loop_idx]["passing_bad_throw_pct"]
            times_blitzed_count += player_history.iloc[loop_idx]["times_blitzed"]
            times_hurried_count += player_history.iloc[loop_idx]["times_hurried"]
            times_hit_count += player_history.iloc[loop_idx]["times_hit"]
            times_pressured_count += player_history.iloc[loop_idx]["times_pressured"]
            times_pressured_pct_count += player_history.iloc[loop_idx]["times_pressured_pct"]
            rushing_yards_before_contact_count += player_history.iloc[loop_idx]["rushing_yards_before_contact"]
            rushing_yards_before_contact_avg_count += player_history.iloc[loop_idx]["rushing_yards_before_contact_avg"]
            rushing_yards_after_contact_count += player_history.iloc[loop_idx]["rushing_yards_after_contact"]
            rushing_yards_after_contact_avg_count += player_history.iloc[loop_idx]["rushing_yards_after_contact_avg"]
            rushing_broken_tackles_count += player_history.iloc[loop_idx]["rushing_broken_tackles"]'''

            loop_idx-=1

            if(loop_idx<0):
                loop_idx = curr_id_count-1

            count+=1
        curr_id_count+=1

        qb_nn.at[i,"completions"] = completions_count/game_coverage
        qb_nn.at[i,"attempts"] = attempts_count/game_coverage
        qb_nn.at[i,"passing_yards"] = passing_yards_count/game_coverage
        qb_nn.at[i,"passing_tds"] = passing_tds_count/game_coverage
        qb_nn.at[i,"interceptions"] = interceptions_count/game_coverage
        qb_nn.at[i,"sacks"] = sacks_count/game_coverage
        qb_nn.at[i,"sack_fumbles"] = sack_fumbles_count/game_coverage
        qb_nn.at[i,"passing_air_yards"] = passing_air_yards_count/game_coverage
        qb_nn.at[i,"passing_yards_after_catch"] = passing_yards_after_catch_count/game_coverage
        qb_nn.at[i,"passing_first_downs"] = passing_first_downs_count/game_coverage
        qb_nn.at[i,"passing_epa"] = passing_epa_count/game_coverage
        qb_nn.at[i,"passing_2pt_conversions"] = passing_2pt_conversions_count/game_coverage
        qb_nn.at[i,"pacr"] = pacr_count/game_coverage
        qb_nn.at[i,"dakota"] = dakota_count/game_coverage
        qb_nn.at[i,"carries"] = carries_count/game_coverage
        qb_nn.at[i,"rushing_yards"] = rushing_yards_count/game_coverage
        qb_nn.at[i,"rushing_tds"] = rushing_tds_count/game_coverage
        qb_nn.at[i,"rushing_fumbles"] = rushing_fumbles_count/game_coverage
        qb_nn.at[i,"rushing_first_downs"] = rushing_first_downs_count/game_coverage
        qb_nn.at[i,"rushing_epa"] = rushing_epa_count/game_coverage
        qb_nn.at[i,"rushing_2pt_conversions"] = rushing_2pt_conversions_count/game_coverage
        qb_nn.at[i,"fantasy_points_historical"] = fantasy_points_historical_count/game_coverage

        qb_nn.at[i,"snap_count"] = snap_count_count/game_coverage

        '''qb_nn.at[i,"avg_time_to_throw"] = avg_time_to_throw_count/game_coverage
        qb_nn.at[i,"avg_completed_air_yards"] = avg_completed_air_yards_count/game_coverage
        qb_nn.at[i,"avg_intended_air_yards"] = avg_intended_air_yards_count/game_coverage
        qb_nn.at[i,"avg_air_yards_differential"] = avg_air_yards_differential_count/game_coverage
        qb_nn.at[i,"aggressiveness"] = aggressiveness_count/game_coverage
        qb_nn.at[i,"max_completed_air_distance"] = max_completed_air_distance_count/game_coverage
        qb_nn.at[i,"avg_air_yards_to_sticks"] = avg_air_yards_to_sticks_count/game_coverage
        qb_nn.at[i,"passer_rating"] = passer_rating_count/game_coverage
        qb_nn.at[i,"completion_percentage"] = completion_percentage_count/game_coverage
        qb_nn.at[i,"expected_completion_percentage"] = expected_completion_percentage_count/game_coverage
        qb_nn.at[i,"completion_percentage_above_expectation"] = completion_percentage_above_expectation_count/game_coverage
        qb_nn.at[i,"avg_air_distance"] = avg_air_distance_count/game_coverage
        qb_nn.at[i,"max_air_distance"] = max_air_distance_count/game_coverage

        qb_nn.at[i,"passing_drops"] = passing_drops_count/game_coverage
        qb_nn.at[i,"passing_drop_pct"] = passing_drop_pct_count/game_coverage
        qb_nn.at[i,"passing_bad_throws"] = passing_bad_throws_count/game_coverage
        qb_nn.at[i,"passing_bad_throw_pct"] = passing_bad_throw_pct_count/game_coverage
        qb_nn.at[i,"times_blitzed"] = times_blitzed_count/game_coverage
        qb_nn.at[i,"times_hurried"] = times_hurried_count/game_coverage
        qb_nn.at[i,"times_hit"] = times_hit_count/game_coverage
        qb_nn.at[i,"times_pressured"] = times_pressured_count/game_coverage
        qb_nn.at[i,"times_pressured_pct"] = times_pressured_pct_count/game_coverage
        qb_nn.at[i,"rushing_yards_before_contact"] = rushing_yards_before_contact_count/game_coverage
        qb_nn.at[i,"rushing_yards_before_contact_avg"] = rushing_yards_before_contact_avg_count/game_coverage
        qb_nn.at[i,"rushing_yards_after_contact"] = rushing_yards_after_contact_count/game_coverage
        qb_nn.at[i,"rushing_yards_after_contact_avg"] = rushing_yards_after_contact_avg_count/game_coverage
        qb_nn.at[i,"rushing_broken_tackles"] = rushing_broken_tackles_count/game_coverage'''
    
    qb_nn.at[i,"fantasy_points"] = data["fantasy_points"]

qb_nn.drop(data_to_drop, inplace=True)
qb_nn.reset_index(drop=True, inplace=True)

qb_nn.fillna(0, inplace=True)

print(qb_nn.head())

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