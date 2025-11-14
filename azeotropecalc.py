import joblib
import requests
import pandas as pd

class AzeotropeCalc:
    OWM_API_KEY = '9adced7ddff5c6dc7f031455d3dec00e'
    model = joblib.load('model.pkl')

    @staticmethod
    def get_weather_data(lat, lon):
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={AzeotropeCalc.OWM_API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            pressure_hPa = data['main']['pressure']
            pressure_mmHg = round(pressure_hPa * 0.75006, 2)
            
            weather_info = {
                'pressure_mmHg': pressure_mmHg,
                'temperature': round(data['main']['temp'], 1),
                'humidity': data['main']['humidity'],
                'weather_desc': data['weather'][0]['description'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # convert m/s to km/h
                'city_name': data.get('name', 'نامشخص'),
                'error': None
            }
            return weather_info
        else:
            return {'error': "خطا در دریافت اطلاعات آب و هوا"}

    @staticmethod
    def predict_temperature(pressure):
        input_data = pd.DataFrame({'mmhg': [pressure]})
        predicted_temp = AzeotropeCalc.model.predict(input_data)[0]
        return round(predicted_temp, 2)

    @staticmethod
    def calculate(data):
        try:
            lat = float(data.get('lat'))
            lon = float(data.get('lon'))
            
            weather_data = AzeotropeCalc.get_weather_data(lat, lon)
            if weather_data.get('error'):
                return weather_data
            
            azeotrope_temp = AzeotropeCalc.predict_temperature(weather_data['pressure_mmHg'])
            
            return {
                'pressure': weather_data['pressure_mmHg'],
                'temperature': azeotrope_temp,
                'current_temp': weather_data['temperature'],
                'humidity': weather_data['humidity'],
                'weather_desc': weather_data['weather_desc'],
                'wind_speed': weather_data['wind_speed'],
                'city_name': weather_data['city_name'],
                'error': None
            }
        except Exception as e:
            return {"error": "خطا در محاسبات. لطفا دوباره تلاش کنید."}