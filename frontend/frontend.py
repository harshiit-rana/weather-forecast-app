import streamlit as st
import requests

st.set_page_config(page_title="Weather App", layout="centered")

st.markdown("## 🌦️ Real-Time Weather App")

city = st.text_input("Enter a city name:", "Delhi")

if st.button("Get Weather"):
    with st.spinner("Fetching weather data..."):
        try:
            params = {"city": city}
            response = requests.get("https://weather-backend-harshit.azurewebsites.net/api/weather", params=params)

            data = response.json()

            if "error" in data:
                st.error(data["error"])
            else:
                # -- TODAY'S WEATHER --
                today = data["today"]
                st.markdown(f"### ☀️ Weather in {city.title()} (Today)")
                st.image(f"http://openweathermap.org/img/wn/{today['icon']}@2x.png", width=100)
                st.write(f"🌡️ **Temperature**: {today['temperature']}°C")
                st.write(f"⛅ **Description**: {today['description']}")
                st.write(f"💧 **Humidity**: {today['humidity']}%")
                st.write(f"🌬️ **Wind Speed**: {today['wind_speed']} m/s")

                # -- TOMORROW'S WEATHER --
                tomorrow = data.get("tomorrow")
                if tomorrow:
                    st.markdown(f"### 🌤️ Forecast for Tomorrow")
                    st.image(f"http://openweathermap.org/img/wn/{tomorrow['icon']}@2x.png", width=100)
                    st.write(f"🌡️ **Temperature**: {tomorrow['temperature']}°C")
                    st.write(f"⛅ **Description**: {tomorrow['description']}")
                    st.write(f"💧 **Humidity**: {tomorrow['humidity']}%")
                    st.write(f"🌬️ **Wind Speed**: {tomorrow['wind_speed']} m/s")
                else:
                    st.warning("Tomorrow's forecast is not available.")
        except Exception as e:
            st.error(f"Error: {e}")
