import json
import urllib.request as request
import datetime

api_key = '&APPID=9b804c03cd199973cd5a9a98b80b0f10'
units = '&units=metric'
city = input("Enter name of city: ")

url = 'http://api.openweathermap.org/data/2.5/weather?q={0}{1}'.format(city, units)
query = request.urlopen(url + api_key).read().decode('utf-8')
query_json = json.loads(query)
print('https://www.google.com.ua/maps/place/{0}+{1}'.format(query_json['coord']['lat'], query_json['coord']['lon']))

temperature = query_json['main']['temp']
humidity = str(query_json['main']['humidity']) + '%'
wind = str(query_json['wind']['speed']) + ' km/h'
sun_rise = datetime.datetime.fromtimestamp(query_json['sys']['sunrise']).strftime('%H:%M:%S')
sun_set = datetime.datetime.fromtimestamp(query_json['sys']['sunset']).strftime('%H:%M:%S')
pressure = str(query_json['main']['pressure']) + ' hPa'
weather = str(query_json['weather'][0]['main']) + ' '
print(
    '\t {0}°C {1} {2} {3} sun rise: {4}, sun set: {5}'.format(temperature, pressure, wind, humidity, sun_rise, sun_set))

# weather on 16 days
DAYS = 16
url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={0}&mode=json{1}&cnt={2}'.format(city, units, DAYS)

query = request.urlopen(url + api_key).read().decode('utf-8')
query_json = json.loads(query)

print("Weather on 16 days: ")
for day in query_json['list']:
    humidity = str(day['humidity']) + '%'
    pressure = str(day['pressure']) + ' hPa'
    temperature = {'day': day['temp']['day'],
                   'evening': day['temp']['eve'],
                   'morning': day['temp']['morn'],
                   'night': day['temp']['night'],
                   'min': day['temp']['min'],
                   'max': day['temp']['max']}
    date = datetime.datetime.fromtimestamp(day['dt']).strftime('%d-%m')
    wind = str(day['speed']) + ' km/h'
    weather = str(day['weather'][0]['main'])
    print('\t', date, weather, pressure, humidity, wind)
    for key in temperature:
        print('\t\t\t{0}: {1}°C'.format(key, temperature[key]))
input()
