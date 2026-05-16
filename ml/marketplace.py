import json
import os

FILE = "data/listings.json"

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_listing(data):
    listings = load_data()
    listings.append(data)
    save_data(listings)

def get_listings():
    return load_data()

def delete_listing(index):
    data = load_data()
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)

def update_listing(index, new_data):
    data = load_data()
    if 0 <= index < len(data):
        data[index] = new_data
        save_data(data)