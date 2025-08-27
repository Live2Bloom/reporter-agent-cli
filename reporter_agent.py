import requests
import sys

class ReporterAgent:
    
    def __init__(self, city, topic):
        self._city = city
        self._topic = topic
        self._report = None

    def __str__(self):
        return f"<ReporterAgent for {self._city}, Topic: {self._topic}>"
    
    @property
    def city(self):
        return self._city

    @property
    def topic(self):
        return self._topic
    
    def get_data(self):
        try:
            if self._topic == "weather":
                api_key= "0b8395331df74668a32210650252508"
                url= "https://api.weatherapi.com/v1/current.json"
                params = {
                    "key": api_key,
                    "q": self._city
                }
                response = requests.get(url, params= params)
                response.raise_for_status()
                weather_data = response.json()
                return weather_data

            elif self._topic == "news":
                api_key= "pub_a1830ffcbaea4076b916bb55db7756e2"
                url= "https://newsdata.io/api/1/latest"
                params = {
                    "apikey": api_key,
                    "q": self._city,
                    "country": "us"
                }
                response = requests.get(url,params=params)
                response.raise_for_status()
                news_data = response.json()
                return news_data

            elif self._topic == "events":
                api_key= "pub_a1830ffcbaea4076b916bb55db7756e2"
                url= "https://newsdata.io/api/1/latest"
                params = {
                    "apikey": api_key,
                    "q": f"{self._city} events",
                    "country": "us"
                }
                response = requests.get(url,params=params)
                response.raise_for_status()
                events_data = response.json()
                return events_data

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to API: {e}")
            return None

    def generate_report(self, report_data):
        if self._topic == "weather":
            region = report_data["location"]["region"]
            country = report_data["location"]["country"]
            local_time = report_data["current"]["last_updated"]
            current_temp = report_data["current"]["temp_f"]
            condition = report_data["current"]["condition"]["text"]
            wind_speed = report_data["current"]["wind_mph"]
            humidity = report_data["current"]["humidity"]
            report = f"Local Weather for {region}, {country}: It is {current_temp}F and {condition} with a wind speed of {wind_speed} MPH and {humidity}% humidity. Report as of {local_time}"
            return report

        elif self._topic == "news":
            news_list = []
            for result in report_data["results"]:
                news_title = result["title"]
                news_link = result["link"]
                news_description = result["description"]
                news_report = f"Breaking News: {news_title} \nSummary: {news_description} \nRead More: {news_link}"
                news_list.append(news_report)
            return "\n".join(news_list)

        elif self._topic == "events":
            events_list = []
            for result in report_data["results"]:
                event_title = result["title"]
                event_link = result["link"]
                event_description = result["description"]
                event_report = f"Local Event: {event_title} \nSummary: {event_description} \nFind out more: {event_link}"
                events_list.append(event_report)
            return "\n".join(events_list)
    
    def save_report(self, report):
        file_name = f"{self._city.replace(' ', '_')}_{self._topic}_report.txt"
        with open(file_name, "w") as file:
            file.write(report)
        print(f"Report saved to {file_name}")