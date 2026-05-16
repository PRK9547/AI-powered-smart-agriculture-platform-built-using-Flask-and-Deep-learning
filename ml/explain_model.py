def explain_crop(soil, season, rainfall, temperature, humidity, crop):

    explanation = []

    explanation.append(f"The selected soil type ({soil}) supports cultivation of {crop}.")
    explanation.append(f"The {season.capitalize()} season is suitable for growing {crop}.")

    if rainfall > 200:
        explanation.append("The district has high rainfall which supports water-intensive crops.")
    elif rainfall > 100:
        explanation.append("The rainfall level is moderate and suitable for seasonal crops.")
    else:
        explanation.append("Low rainfall favors drought-resistant crops.")

    explanation.append("Temperature range is favorable for crop growth.")
    explanation.append("Humidity level supports healthy crop development.")

    return explanation