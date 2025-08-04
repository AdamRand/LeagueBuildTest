
import requests
import pandas as pd
import json
from constants import map_number, summoners_rift_items_file

def fetch_and_save_item_data():
    try:
        print("Attempting to fetch data from Riot API...")
        version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
        item_data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json").json()["data"]
        items_list = []

        for item_id, item in item_data.items():
            if item.get("maps", {}).get(map_number, False) and item.get("inStore", True):
                items_list.append({
                    "id": item_id,
                    "name": item.get("name", ""),
                    "description": item.get("description", "")
                        .replace("<br>", " ").replace("<li>", "- ").replace("</li>", "")
                        .replace("<mainText>", "").replace("</mainText>", "")
                        .replace("<attention>", "").replace("</attention>", ""),
                    "gold_total": item.get("gold", {}).get("total", 0),
                    "gold_base": item.get("gold", {}).get("base", 0),
                    "gold_sell": item.get("gold", {}).get("sell", 0),
                    "tags": ",".join(item.get("tags", [])),
                    "stats": json.dumps(item.get("stats", {}))
                })

        pd.DataFrame(items_list).to_csv(summoners_rift_items_file, index=False)
        print("Fresh item data saved.")
    except Exception as e:
        print(f"Could not fetch data from Riot API. Reason: {e}")
        print("Falling back to local data.")