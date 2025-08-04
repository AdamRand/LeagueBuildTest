
from riot_api import fetch_and_save_item_data
from item_utils import load_items, combine_item_stats, display_stats
from armor_calc import calculate_effective_armor
from constants import *
import pandas as pd

# Fetch Riot data or use fallback
fetch_and_save_item_data()

# Load item data
df = pd.read_csv(summoners_rift_items_file)
df["gold_total"] = pd.to_numeric(df["gold_total"], errors="coerce")

# Filter top 71 + boots
top_71 = df.sort_values(by="gold_total", ascending=False).head(71)
boots = df[df["name"].isin(upgraded_boot_names)]
final_items = pd.concat([top_71, boots]).drop_duplicates(subset="id")
final_items.to_csv(legendary_and_boots, index=False)

# Random build selection
legendary_df = final_items[~final_items["name"].isin(upgraded_boot_names)]
boots_df = final_items[final_items["name"].isin(upgraded_boot_names)]
selected_legendary = legendary_df.sample(n=5)
selected_boot = boots_df.sample(n=1)
final_build = pd.concat([selected_legendary, selected_boot]).reset_index(drop=True)
final_build.to_csv(final_item_build_file, index=False)

# Combine and display stats
item_data_dict = load_items(legendary_and_boots)
build_ids = final_build["id"].astype(str).tolist()
total_stats = combine_item_stats(item_data_dict, build_ids)

print("\nFinal Build (5 Legendary + 1 Boots):")
print(final_build[["name", "gold_total"]])
display_stats(total_stats)

armor = calculate_effective_armor(base_armor, bonus_armor, flat_reduction, flat_pen, percent_reduction, percent_pen)
print(f"\nFinal Effective Armor: {armor}")
print(71*70*69*68*67*7)
