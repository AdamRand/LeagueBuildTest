# Import necessary libraries
from flask import Flask, request, jsonify, render_template  # Flask for web app, request/response handling
import pandas as pd  # Pandas for reading and handling CSV data
from armor_calc import calculate_effective_armor  # Custom function to compute final armor
from item_utils import load_items, combine_item_stats  # Functions to load and process item stats
from constants import final_item_build_file, stat_names  # File paths and stat labels from constants.py

# Create a Flask web application instance
app = Flask(__name__)

# Define the route for the home page
@app.route("/")
def index():
    # Render the index.html template from the 'templates' folder
    return render_template("index.html")

# Define a POST route to calculate stats and armor based on user input
@app.route("/calculate", methods=["POST"])
def calculate():
    # Get the JSON data sent from the frontend form
    data = request.json

    # Extract and convert each input field from the form, with default fallbacks
    base = float(data.get("base_armor", 0))
    bonus = float(data.get("bonus_armor", 0))
    flat_red = float(data.get("flat_reduction", 0))
    flat_pen = float(data.get("flat_pen", 0))
    percent_red = float(data.get("percent_reduction", 0))
    percent_pen = float(data.get("percent_pen", 0))

    # Read the current final build CSV file (5 legendary + 1 boots) into a DataFrame
    df = pd.read_csv(final_item_build_file)

    # Extract item IDs from the build
    build_ids = df["id"].astype(str).tolist()

    # Load item stats from CSV and compute total combined stats for the selected build
    item_data_dict = load_items(final_item_build_file)
    total_stats = combine_item_stats(item_data_dict, build_ids)

    # Calculate the effective armor using the imported formula
    effective_armor = calculate_effective_armor(base, bonus, flat_red, flat_pen, percent_red, percent_pen)

    # Format stats for frontend display (e.g., convert 0.2 to 20% for percent stats)
    readable_stats = {
        stat_names.get(k, k): round(v * 100 if "Percent" in k else v, 2)
        for k, v in total_stats.items()
    }

    # Return all data as JSON back to the frontend
    return jsonify({
        "build": df.to_dict(orient="records"),       # Full table data for item build
        "columns": df.columns.tolist(),              # Column names (headers)
        "total_stats": readable_stats,               # Total combined stats
        "effective_armor": effective_armor           # Final armor value after all reductions/penetrations
    })

# Run the app when this file is executed directly (development mode only)
if __name__ == '__main__':
    app.run(debug=True)  # debug=True enables auto-reload and better error messages
