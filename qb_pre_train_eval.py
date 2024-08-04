import pandas as pd

qb_nn = pd.read_csv("nn_data/qb_nn.csv")

# Create a coorelation matrix to see which features are most important
# Don't include "ID" or "2023" in the matrix
#qb_nn = qb_nn[qb_nn["2023"] == 1]
qb_nn = qb_nn.drop(columns=["id","2023"])
correlation_matrix = qb_nn.corr()
pd.set_option('display.max_rows', None)
print(correlation_matrix["fantasy_points"].sort_values(ascending=False))

# Plot correlation matrix fantasy points as a bar graph
import matplotlib.pyplot as plt
# Sort the values in the bar graph
correlation_matrix = correlation_matrix.sort_values(by="fantasy_points",ascending=False)
correlation_matrix["fantasy_points"].plot(kind='bar')
plt.title("Correlation Matrix for QB Fantasy Points")
plt.ylabel("Correlation Value")
plt.xlabel("Feature")
plt.show()



'''
RESULTS

1. fantasy_points_historial: 0.313465
    - Historical fantasy points scored by the player, naturally, gives by FAR the best estimate of their future fantasy points scored
2. passing_epa: 0.229575
    - "Expected points" added by the player's passing plays
3. dakota: 0.220757
    - A composite score of expected points and completion percentage over expected
4. carries: 0.206573
    - The number of carries the player has had; shows that rushing QBs are VERY valuable
5. rushing_yards: 0.204754
    - Again, shows that rushing QBs are VERY valuable
6. passing_tds: 0.203714
7. passer_rating: 0.202471
    - QBR Rating
8. rushing_first_downs: 0.198829
9. passing_first_downs: 0.177221
    - Notice how passing first downs are less important than rushing first downs, likely due to the dual threat nature of rushing QBs being very valuable for fantasy points
10. passing_yards: 0.172339
11. rushing_tds: 0.161103
    - Given the trends listed above, it's interesting that rushing TDs are less important than passing TDs. This could be due to the fact that rushing TDs are more rare than passing TDs, so they are less predictable
12. rushing_epa: 0.149423
    - "Expected points" added by the player's rushing plays. Significantly less important than passing EPA
13. max_air_distance: 0.140932
    - Possibly valuable since it shows the QBs tendency to throw deep balls for large chunk plays
14. completion_percentage: 0.126694
15. passing_air_yards: 0.124536
    - Significantly less important than base passing yards
16. passing_yards_after_catch: 0.117228
17. completions: 0.113158
    - Significantly less important than completion percentage
18. avg_completed_air_yards: 0.110301
19. avg_air_yards_to_sticks: 0.109612
20. completion_percentage_above_expectation: 0.106517
21. snap_count: 0.102657
22. max_completed_air_distance: 0.102383
23. avg_intended_air_yards: 0.101052
24. interceptions: -0.098295
25. aggressiveness: -0.109377
'''

'''
TO REMOVE (features with low correlation to fantasy points):

opp_passing_yards_allowed                  0.078961
avg_time_to_throw                          0.072456
attempts                                   0.069598
opp_rushing_tds_allowed                    0.068812
expected_completion_percentage             0.067596
rushing_fumbles                            0.066907
avg_air_distance                           0.058375
opp_passing_tds_allowed                    0.057662
opp_rushing_yards_allowed                  0.037029
pacr                                       0.027072
rushing_2pt_conversions                    0.020021
passing_2pt_conversions                    0.016178
opp_receiving_fumbles                      0.013293
avg_air_yards_differential                 0.006282
opp_sack_fumbles_recovered                 0.006103
opp_receiving_fumbles_recovered            0.001306
opp_sack_fumbles                          -0.013888
opp_special_teams_tds_allowed             -0.021645
opp_sacks                                 -0.033727
opp_sack_yards                            -0.038288
sack_fumbles                              -0.043380
sacks                                     -0.045667
opp_interceptions                         -0.050220

'''
