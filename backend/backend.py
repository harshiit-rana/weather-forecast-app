import requests
from datetime import datetime, timedelta  # ✅ This line is required!

API_KEY = "860f66c1cc4aca349cb7fb0a40d4addd"

def fetch_weather(city):
    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    current_res = requests.get(current_url)
    forecast_res = requests.get(forecast_url)

    if current_res.status_code == 200 and forecast_res.status_code == 200:
        current_data = current_res.json()
        forecast_data = forecast_res.json()

        # Current weather
        current_weather = {
            "temperature": current_data["main"]["temp"],
            "description": current_data["weather"][0]["description"].capitalize(),
            "humidity": current_data["main"]["humidity"],
            "wind_speed": current_data["wind"]["speed"],
            "icon": current_data["weather"][0]["icon"]
        }

        # Tomorrow's forecast
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")

        tomorrow_data = next(
            (entry for entry in forecast_data["list"] if entry["dt_txt"].startswith(tomorrow_str)),
            None
        )

        if tomorrow_data:
            tomorrow_weather = {
                "temperature": tomorrow_data["main"]["temp"],
                "description": tomorrow_data["weather"][0]["description"].capitalize(),
                "humidity": tomorrow_data["main"]["humidity"],
                "wind_speed": tomorrow_data["wind"]["speed"],
                "icon": tomorrow_data["weather"][0]["icon"]
            }
        else:
            tomorrow_weather = None

        return {
            "today": current_weather,
            "tomorrow": tomorrow_weather
        }, None
    else:
        return None, "City not found or API error."

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/weather")
def weather_api():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City not provided"}), 400

    weather, error = fetch_weather(city)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(weather)

if __name__ == "__main__":
    app.run(debug=True)