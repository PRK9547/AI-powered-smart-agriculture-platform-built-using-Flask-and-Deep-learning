import pandas as pd

def forecast_crop(crop):

    df = pd.read_csv("data/crop_demand_price_full_realistic_5years.csv")

    df["crop"] = df["crop"].str.lower().str.strip()
    crop = crop.lower().strip()

    crop_df = df[df["crop"] == crop]

    if crop_df.empty:
        return [], "No Data", [], "No Data"

    # Sort by date just to be safe
    crop_df = crop_df.sort_values("date")

    # Take last 6 months
    last_6 = crop_df.tail(6)

    months =[f"Month {i+1}" for i in range(6)]
    demand_values = list(last_6["demand_tons"])
    price_values = list(last_6["price_per_quintal"])

    demand_forecast = list(zip(months, demand_values))
    price_forecast = list(zip(months, price_values))

    demand_trend = "Increasing" if demand_values[-1] > demand_values[0] else "Decreasing"
    price_trend = "Increasing" if price_values[-1] > price_values[0] else "Decreasing"

    return demand_forecast, demand_trend, price_forecast, price_trend