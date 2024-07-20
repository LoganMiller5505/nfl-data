import nfl_data_py as nfl
import pandas as pd

# Set range for years to save CVs of (where first_year is inclusive, and last_year is exclusive)
first_year = 2004
last_year = 2024

# Import raw weekly data
print("Weekly Data Importing . . .\n") #Print status update
weekly = nfl.import_weekly_data(range(first_year,last_year)) #Built in function collecting raw weekly data within year range
weekly = weekly[weekly["season_type"].isin(["REG"])].reset_index(drop=True) #Only take data from regular season (no post season)
print(weekly[0:5]) #Print sample of result
print("\nWeekly Data Imported!\n") #Print status update

id_name_hasmap = {}
for x in weekly["player_id"].unique():
    id_name_hasmap[x] = weekly[weekly["player_id"].isin([x.split(":")[0]])].reset_index(drop=True).at[0,"player_display_name"]

print(id_name_hasmap)

# Save the hashmap to a CSV
id_name_df = pd.DataFrame(id_name_hasmap.items(), columns=["id", "name"])
id_name_df.to_csv("hashmap/hashmap.csv", index=False)