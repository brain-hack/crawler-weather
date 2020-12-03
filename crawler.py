import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from today_weather import TodayChart
from today_weather import TodaySummary
from today_weather import TodayWeather
from today_weather import TimeWeatherItem
from today_weather import TimeWeather
from today_weather import ClimateRain
from today_weather import ClimateHumidity
from today_weather import ClimateWind
from today_weather import TimeClimate
from today_weather import box_item
from today_weather import WeeklyClimate
from today_weather import Weekly

def parse_now_temperature(today_weather_tag):
    now_temperature_tag = today_weather_tag.select_one('div.weather_area > strong')
    now_temperature_without_child_tags = [
        bs_object for bs_object in now_temperature_tag if isinstance(bs_object, NavigableString)
    ]
    now_temperature = "".join(now_temperature_without_child_tags)
    return now_temperature

def parse_today_summary_text(today_weather_tag):
    today_summary = today_weather_tag.select_one('div.weather_area > p')
    return today_summary.text

def parse_today_summary_list(today_weather_tag):
    today_summary_list_tags = today_weather_tag.select('div.weather_area > dl > dd')

    today_summary_list = [today_summary_item_tag.text for today_summary_item_tag in today_summary_list_tags]

    return today_summary_list

def parse_today_summary(today_weather_tag):

    today_summary_text = parse_today_summary_text(today_weather_tag)
    today_summary_list = parse_today_summary_list(today_weather_tag)

    return TodaySummary(today_summary_text,today_summary_list)

def parse_today_chart_list(today_weather_tag):

    today_chart_value_tags = today_weather_tag.select(
        'div.scroll_control > div > ul > li.item_today > a > div.chart > strong.value')
    today_chart_level_tags = today_weather_tag.select(
        'div.scroll_control > div > ul > li.item_today > a > div.ttl_area > em.level_text')

    today_chart_value_list = [today_chart_value_item_tag.text for today_chart_value_item_tag in today_chart_value_tags]
    today_chart_level_list = [today_chart_level_item_tag.text for today_chart_level_item_tag in today_chart_level_tags]

    return TodayChart(today_chart_value_list, today_chart_level_list)

def parse_update_time(time_weather_tag):
    return time_weather_tag.select_one('div.top_area > span').text

def parse_time_weather_item(time_weather_item_tag):
    time = time_weather_item_tag.select_one('span.time').text
    weather = time_weather_item_tag.select_one('i > span.blind').text
    temperature = time_weather_item_tag.select('span.blind')[1].text
    return TimeWeatherItem(time,weather,temperature)


def parse_time_weather(time_weather_tag):
    update_time = parse_update_time(time_weather_tag)

    list_time_weather_tags = time_weather_tag.select('div.scroll_control.end_left > div > div > ul > li')
    list_time_weather = [parse_time_weather_item(time_weather_item_tag) for time_weather_item_tag in list_time_weather_tags]

    return TimeWeather(update_time,list_time_weather)

def parse_today_weather(soup):
    today_card_tag = soup.select_one('#content > div > div.card.card_today')
    today_weather_tag = today_card_tag.select_one('div.today_weather')
    time_weather_tag = today_card_tag.select_one('div.time_weather')

    now_temperature = parse_now_temperature(today_weather_tag)
    today_summary = parse_today_summary(today_weather_tag)
    today_chart = parse_today_chart_list(today_weather_tag)
    time_weather = parse_time_weather(time_weather_tag)

    return TodayWeather(now_temperature,today_summary,today_chart,time_weather)

def parse_time_climate_rain(hourly_tag):
    climate_rain_table = hourly_tag.select_one('div.inner_card.climate_rain > div > div.scroll_area > table > tbody')

    climate_rain_probabilities_tags = climate_rain_table.select('tr.row_icon > td.data > em.value')
    climate_rain_probabilities = [climate_rain_probability_tag.text for climate_rain_probability_tag in climate_rain_probabilities_tags]

    climate_rain_value_td_tags = climate_rain_table.select('tr.row_graph > td.data')
    climate_rain_values = []
    for climate_rain_value_td in climate_rain_value_td_tags:
        climate_rain_value_tag = climate_rain_value_td.select_one('div.data_inner')
        climate_rain_value = climate_rain_value_tag.text.strip()
        if 'colspan' in climate_rain_value_td.attrs:
            for i in range(int(climate_rain_value_td['colspan'])):
                climate_rain_values.append(climate_rain_value)
        else:
            climate_rain_values.append(climate_rain_value)

    climate_rain_times_tags = climate_rain_table.select('tr > td.time')
    climate_rain_times = [climate_rain_time_tag.text.strip() for climate_rain_time_tag in climate_rain_times_tags]

    return [ClimateRain(climate_rain_time, climate_rain_probability, climate_rain_value) for climate_rain_time, climate_rain_probability, climate_rain_value
             in zip(climate_rain_times,climate_rain_probabilities,climate_rain_values)]

def parse_time_climate_humidity(hourly_tag):
    climate_humidity_table = hourly_tag.select_one('div.inner_card.climate_humidity.hide > div > div.scroll_area > table > tbody')

    climate_humidities_tags = climate_humidity_table.select('tr.row_graph > td.data > div > span > span')
    climate_humidities = [climate_humiditiy_tag.text for climate_humiditiy_tag in climate_humidities_tags]

    climate_humiditiy_times_tags = climate_humidity_table.select('tr > td.time')
    climate_humiditiy_times = [climate_humiditiy_time_tag.text.strip() for climate_humiditiy_time_tag in climate_humiditiy_times_tags]

    return [ClimateHumidity(climate_humiditiy_time, climate_humiditiy) for climate_humiditiy_time, climate_humiditiy in zip(climate_humiditiy_times, climate_humidities)]

def parse_time_climate_wind(hourly_tag):
    climate_wind_table = hourly_tag.select_one('div.inner_card.climate_wind.hide > div > div.scroll_area > table > tbody')

    climate_wind_direction_tags = climate_wind_table.select('tr.row_icon > td.data > span.value')
    climate_wind_directions = [climate_wind_direction_tag.text for climate_wind_direction_tag in climate_wind_direction_tags]

    climate_wind_velocity_tags = climate_wind_table.select('tr.row_graph > td.data > div > span > span')
    climate_wind_velocities = [climate_wind_velocity_tag.text for climate_wind_velocity_tag in climate_wind_velocity_tags]

    climate_wind_times_tags = climate_wind_table.select('tr > td.time')
    climate_wind_times = [climate_wind_time_tag.text.strip() for climate_wind_time_tag in climate_wind_times_tags]

    return [ClimateWind(climate_wind_time, climate_wind_direction, climate_wind_velocitie) for climate_wind_time, climate_wind_direction, climate_wind_velocitie in zip(climate_wind_times, climate_wind_directions, climate_wind_velocities)]

def parse_time_climate(soup):
    hourly_tag = soup.select_one('#hourly')

    climate_rains = parse_time_climate_rain(hourly_tag)
    climate_humidities = parse_time_climate_humidity(hourly_tag)
    climate_winds = parse_time_climate_wind(hourly_tag)

    return TimeClimate(climate_rains,climate_humidities,climate_winds)

def box_today(box_color):
    today_tags = box_color.select(
        'li.item > span > span > strong.ttl').text
    today_twoone_tags = box_color.select(
        'li.item > span > span > strong.ttl > span.sub').text
    today_rain_tags = box_color.select(
        'li.item > span > span > strong.rainfall > span.blind').text
    today_rainfall_tags = box_color.select(
        'li.item > span > span > strong.rainfall').text
    today_rainfall_i_tags = box_color.select(
        'li.item > span > span > i > span.blind').text
    today_temp_tags = box_color.select(
        'li.item > span > span > span.data > span.blind').text
    today_temp_de_tags = box_color.select(
        'li.item > span > span > span.data').text
    today_temp_o_tags = box_color.select(
        'li.item > span > span > span.data > span.degree').text
    return [box_item(today_tags,today_twoone_tags,today_rain_tags,today_rainfall_tags,today_rainfall_i_tags,today_temp_tags,today_temp_de_tags,today_temp_o_tags)
           for today_tags,today_twoone_tags,today_rain_tags,today_rainfall_tags,today_rainfall_i_tags,today_temp_tags,today_temp_de_tags,today_temp_o_tags
           in zip(today_tags,today_twoone_tags,today_rain_tags,today_rainfall_tags,today_rainfall_i_tags,today_temp_tags,today_temp_de_tags,today_temp_o_tags)]

def scroll(scroll):
    scroll_values = []
    for scroll_value_li in scroll:
        cell_date = scroll_value_li.select_one('div > div.cell_date > span')
        cell_weather = scroll_value_li.select_one('div > div.cell_weather > span')
        cell_temperature = scroll_value_li.select_one('div > div.cell_temperature > span')
        scroll_value = scroll_value_tag.text.strip()
        if 'colspan' in scroll_value_li.attrs:
            for i in range(int(scroll_value_li['colspan'])):
                scroll_values.append(scroll_value)
        else:
            scroll_values.append(scroll_value)

    return [WeeklyClimate(cell_date, cell_weather, cell_temperature) for cell_date, cell_weather, cell_temperature
            in zip(cell_date, cell_weather, cell_temperature)]

def parse_weekly(soup):
    weekly_tag = soup.select_one('#weekly')

    box_color = weekly_tag.select_one('ul.box_color')
    scroll = weekly_tag.select_one('div.scroll_control end_left > div.scroll_area > ul.week_list')

    week_box_color = box_today(box_color)
    week_scroll = scroll(scroll)

    return Weekly(week_box_color,week_scroll)

def crawl():
    url = 'https://weather.naver.com/'

    res = requests.get(url)

    html = res.text

    #svg tag를 위한 xml 파서
    soup = BeautifulSoup(html,'lxml')

    today_weather = parse_today_weather(soup)
    print(today_weather)

    time_climate = parse_time_climate(soup)
    print(time_climate)

    weekly = parse_weekly(soup)
    print(weekly)

if __name__ == "__main__":
    crawl()