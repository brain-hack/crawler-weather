class TodayChart:

    def __init__(self,today_chart_value_list,today_chart_level_list):

        self.fine_dust_level = today_chart_level_list[0]
        self.ultrafine_dust_level = today_chart_level_list[1]
        self.ultraviolet_ray_level = today_chart_level_list[2]
        self.sunrise_time = today_chart_level_list[3]

        self.fine_dust_value = today_chart_value_list[0]
        self.ultrafine_dust_value = today_chart_value_list[1]
        self.ultraviolet_ray_value = today_chart_value_list[2]


    def __str__(self):
        return f'미세먼지\t{self.fine_dust_level}\t{self.fine_dust_value}\n' \
               f'초미세먼지\t{self.ultrafine_dust_level}\t{self.ultrafine_dust_value}\n' \
               f'자외선\t\t{self.ultraviolet_ray_level}\t{self.ultraviolet_ray_value}\n' \
               f'일출시간\t{self.sunrise_time}\n' \

class TodaySummary:

    def __init__(self,today_summary,today_summary_list):
        self.today_summary = today_summary
        self.desc_feeling = today_summary_list[0]
        self.desc_rainfall = today_summary_list[1]
        self.desc_wind = today_summary_list[2]
        self.desc_humidity = today_summary_list[3]

    def __str__(self):
        return f'{self.today_summary}\n'\
               f'체감온도\t{self.desc_feeling}\n' \
               f'강수확률\t{self.desc_rainfall}\n' \
               f'풍속(방향)\t{self.desc_wind}\n' \
               f'습도\t\t{self.desc_humidity}\n'

class TimeWeatherItem:
    def __init__(self,time,weather,temperature):
        self.time = time
        self.weather_text = weather
        self.temperature = temperature

    def __str__(self):
        return f'{self.time}\t\t{self.weather_text}    \t\t{self.temperature}\n'

class TimeWeather:
    def __init__(self,update_time,list_time_weather):
        self.update_time = update_time
        self.list_time_weather = list_time_weather

    def __str__(self):
        update_time_text = f'{self.update_time}\n' \
               f'---------------------------\n'
        return update_time_text + \
               ''.join([str(time_weather_item) for time_weather_item in self.list_time_weather])

class ClimateRain:
    def __init__(self, time, probability, value):
        self.time = time
        self.probability = probability
        self.value = value

class ClimateHumidity:
    def __init__(self, time, value):
        self.time = time
        self.value = value

class ClimateWind:
    def __init__(self, time, direction, value):
        self.time = time
        self.direction = direction
        self.value = value

class TimeClimateItem:
    def __init__(self, climate_rain, climate_humidity, climate_wind):
        self.climate_rain = climate_rain
        self.climate_humidity = climate_humidity
        self.climate_wind = climate_wind

    def __str__(self):
        return f'{self.climate_rain.time}\t' \
               f'{self.climate_rain.probability}\t\t' \
               f'{self.climate_rain.value}\t' \
               f'{self.climate_humidity.value}\t' \
               f'{self.climate_wind.direction}\t' \
               f'{self.climate_wind.value}\n'

class TimeClimate:
    def __init__(self, list_climate_rain, list_climate_humidity, list_climate_wind):

        self.list_climate = [
            TimeClimateItem(climate_rain, climate_humidity, climate_wind)
            for climate_rain, climate_humidity, climate_wind
            in zip(list_climate_rain,list_climate_humidity,list_climate_wind)
        ]

    def __str__(self):
        return '시간\t강수확률\t강수량\t습도\t풍향\t풍속\n' + \
               ''.join([str(time_climate_item) for time_climate_item in self.list_climate])

class TodayWeather:
    def __init__(self,now_temperature,today_summary,today_chart,time_weather):

        self.now_temperature = now_temperature
        self.today_summary = today_summary
        self.today_chart = today_chart
        self.time_weather = time_weather
        self.time_climate = ''

    def __str__(self):
        return f'{self.now_temperature}\n' \
               f'============================\n' \
               f'{self.today_summary}' \
               f'============================\n' \
               f'{self.today_chart}' \
               f'============================\n' \
               f'{self.time_weather}' \
               f'============================\n' \
               f'{self.time_climate}'

    def add_time_climate(self,time_climate):
        self.time_climate = time_climate