
import requests
from datetime import datetime

def fetch_time_information(city=None, time_zone_name=None):
    try:
        response = requests.get(f"https://timeapi.io/api/Time/current/zone?timeZone={time_zone_name}/{city}")
        response.raise_for_status()
        data = response.json()
        time_info = f"""The Date and Time in {city} is: 
            - date: {data['year']}/{data['month']}/{data['day']}
            - time: {data['hour']}:{data['minute']}:{data['seconds']}
        """
        print("time_info: ", time_info)
        return time_info
    except requests.RequestException:
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y/%m/%d")
        formatted_time = current_datetime.strftime("%H:%M:%S")

        return f"The current date time is:\n  - date: {formatted_date}\n  - time: {formatted_time}"

