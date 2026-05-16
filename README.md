# AI-powered-smart-agriculture-platform-built-using-Flask and Deep learning
It is an AI-powered agriculture platform built with Flask. It provides crop prediction, weather-based recommendations, demand forecasting, and a farmer marketplace with WhatsApp contact integration to help farmers make smarter farming and selling decisions.


# Project Structure
```AI-powered-smart-agriculture-platform-built-using-Flask and Deep learning/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── app.db
│   ├── india_major_district_rainfall.csv
│   ├── crop_dataset_final.csv
│   ├── crop_demand_price_5years.csv
│   └── marketplace.csv
│
├── models/
│   ├── crop_model.pkl
│   └── crop_labels.pkl
│
├── ml/
│   ├── forecast_demand.py
│   └── explain_model.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── predict.html
│   ├── result.html
│   ├── market.html
│   ├── add_listing.html
│   ├── edit_listing.html
│   └── forecast.html
│
└── screenshots/
    ├── dashboard.png
    ├── marketplace.png
    └── prediction.png
```

# Features
```
Crop Recommendation
Weather-based Prediction
Demand Forecasting
Farmer Marketplace
WhatsApp Contact Integration
```

# Technologies Used
```
Python
Flask
Machine Learning
SQLite
HTML/CSS
JavaScript
```

# Run Project
```
pip install -r requirements.txt
python app.py
```
