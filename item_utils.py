
import csv
import json
from collections import defaultdict
from constants import stat_names

def load_items(csv_path):
    items = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stats = json.loads(row["stats"]) if row["stats"] else {}
            items[row["id"]] = stats
            items[row["name"]] = stats
    return items

def combine_item_stats(items_dict, selected_items):
    total_stats = defaultdict(float)
    for item in selected_items:
        if item in items_dict:
            for stat, value in items_dict[item].items():
                total_stats[stat] += value
    return dict(total_stats)

def display_stats(total_stats):
    print("\nTotal Build Stats:")
    for stat, value in total_stats.items():
        label = stat_names.get(stat, stat)
        if "Percent" in stat:
            value = round(value * 100, 2)
        print(f"{label}: {round(value, 2)}")