import requests
from django.conf import settings

def get_weather(lat, lon):
    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('cod') == 200:
            weather = {
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'city': data['name']
            }
            return weather
    except:
        pass
    return None
