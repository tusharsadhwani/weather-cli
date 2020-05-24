"""Test"""
from datetime import datetime
import json
import sys
import urllib.request

TABLE = (
    '             ┌───────────────────────┐               \n'
    '┌────────────┤  {0:^19}  ├────────────┐\n'
    '│            └───────────────────────┘            │\n'
    '├─────────────────────────────────────────────────┤\n'
    '│   {6:11}   {1:29}   │\n'
    '│   {7:11}   {2:29}   │\n'
    '│   {8:11}   {3:29}   │\n'
    '│   {9:11}   {4:29}   │\n'
    '│   {10:11}   {5:29}   │\n'
    '└─────────────────────────────────────────────────┘\n'
)
ICONS = {
    'partly_cloudy' : '  \\  /\n_ /"".-.\n  \\_(   ).\n  /(___(__)\n ',
    'cloudy' : '\n    .--.\n .-(    ).\n(___.__)__)\n           ',
    'sunny' : '   \\   /\n    .-.\n ― (   ) ―\n    `-’\n   /   \\',
    'light_rain' : '_`/"".-.\n ,\\_(   ).\n  /(___(__)\n    ‘ ‘ ‘ ‘\n   ‘ ‘ ‘ ‘',
    'moderate_rain' : '_`/"".-.\n ,\\_(   ).\n  /(___(__)\n  ‚‘‚‘‚‘‚‘ \n  ‚’‚’‚’‚’',
    'heavy_rain' : '    .-.\n   (   ).\n  (___(__)\n ‚‘‚‘‚‘‚‘\n ‚’‚’‚’‚’',
    'snow' : '    .-.\n   (   ).\n  (___(__)\n  * * * *\n * * * *',
    'haze' : ' \n_ - _ - _ -\n _ - _ - _ \n_ - _ - _ -\n '
}


API_KEY = '471c6ae42588cc6588fbd99a223972a8'

def search_city(cities):
    """Takes input for city name and returns the city ID"""
    city_name = input("Enter city name: ").strip().lower()
    results = []

    for city in cities:
        if city_name in city['name'].lower():
            results.append(city)

    if not results:
        print("No cities found.")
        return search_city(cities)

    for index, city in enumerate(results, 1):
        print(f"{index}. {city['name']}, {city['country']}")

    while True:
        try:
            city_index = int(input('Which one?: '))
            if city_index < 1:
                raise ValueError
            selected_city = results[city_index-1]
            return selected_city['id']
        except KeyboardInterrupt:
            sys.exit()
        except ValueError:
            print('Try again.')
        except IndexError:
            print('Try again.')


def show_weather_info(city_id):
    """Gets the weather info and displays it on stdout"""
    url = f'https://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&id={city_id}'

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())

    display_weather(data)

def get_weather_icon(icon_id):
    """Returns icon name for an icon id"""
    if 200 <= icon_id < 300:
        return 'heavy_rain'

    if 300 <= icon_id < 400:
        return 'light_rain'

    if icon_id == 500:
        return 'light_rain'

    if icon_id == 501:
        return 'moderate_rain'

    if 502 <= icon_id < 600:
        return 'heavy_rain'

    if 600 <= icon_id < 700:
        return 'snow'

    if 700 <= icon_id < 800:
        return 'haze'

    if icon_id == 800:
        return 'sunny'

    if icon_id == 801:
        return 'partly_cloudy'

    if icon_id >= 802:
        return 'cloudy'


def get_celcius(kelvin):
    """Returns celcius value from kelvin input"""
    return round(kelvin - 273.15, 1)


def display_weather(data):
    """Prints weather onto stdout"""
    icon = get_weather_icon(data['weather'][0]['id'])
    date_string = datetime.now().strftime('%a %d %b %I:%M %p')

    weather = TABLE.format(
        date_string,
        data['weather'][0]['description'].title(),
        f"Temperature:     {get_celcius(data['main']['temp'])}°C",
        f"Feels like:      {get_celcius(data['main']['feels_like'])}°C",
        f"Humidity:        {data['main']['humidity']}%",
        f"Wind Speed:      {data['wind']['speed']}m/s",
        *ICONS[icon].splitlines()
    )
    print(weather)


def main():
    """Main interface"""
    with open('cities.json', encoding='utf8') as cities_file:
        cities = json.load(cities_file)

    city_id = search_city(cities)
    print("Getting weather info...")
    show_weather_info(city_id)


if __name__ == "__main__":
    main()
