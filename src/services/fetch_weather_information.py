import requests


def fetch_weather_information(city):
    if city.lower() == "none":
        return ""
    try:
        api_key = "d8dbd7f42fff4fd0b34144008232311"
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}")
        response.raise_for_status()
        data = response.json()

        weather_info = f"""The weather in {city} is: 
            - temperature: {data['current']['temp_c']}
            - humidity: {data['current']['humidity']}
            - wind_speed: {data['current']['wind_kph']}
            - precipitation: {data['current']['precip_mm']}
        """
        print("weather_info: ", weather_info)
        return weather_info
    except requests.RequestException:
        return f"Error: Unable to retrieve weather data for {city}."

