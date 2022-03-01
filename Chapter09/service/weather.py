import os
import datetime

import requests
import json
from requests import ConnectionError, HTTPError, TooManyRedirects, Timeout


KEY = os.getenv("SENIVERSE_KEY", "")  # API key
API = "https://api.seniverse.com/v3/weather/daily.json"  # API URL
UNIT = "c"  # 温度单位
LANGUAGE = "zh-Hans"  # 查询结果的返回语言


one_day_timedelta = datetime.timedelta(days=1)


def fetch_weather(location: str, start=0, days=15) -> dict:
    result = requests.get(
        API,
        params={
            "key": KEY,
            "location": location,
            "language": LANGUAGE,
            "unit": UNIT,
            "start": start,
            "days": days,
        },
        timeout=2,
    )
    return result.json()


def get_weather_by_date(location: str, date: datetime.date) -> dict:
    day_timedelta = date - datetime.datetime.today().date()
    day = day_timedelta // one_day_timedelta

    return get_weather_by_day(location, day)


def get_weather_by_day(location: str, day=1) -> dict:
    result = fetch_weather(location)
    print(result)
    normal_result = {
        "location": result["results"][0]["location"],
        "result": result["results"][0]["daily"][day],
    }

    return normal_result


def get_text_weather_date(address: str, date_time: str, raw_date_time: str) -> str:
    try:
        result = get_weather_by_date(address, date_time)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = "{} {} ({}) 的天气情况为：白天：{}；夜晚：{}；气温：{}-{} 度"
        text_message = text_message_tpl.format(
            result["location"]["name"],
            raw_date_time,
            result["result"]["date"],
            result["result"]["text_day"],
            result["result"]["text_night"],
            result["result"]["high"],
            result["result"]["low"],
        )

    return text_message


if __name__ == "__main__":
    # simple test cases

    default_location = "上海"
    result = fetch_weather(default_location)
    print(json.dumps(result, ensure_ascii=False))

    default_location = "北京"
    result = get_weather_by_day(default_location)
    print(json.dumps(result, ensure_ascii=False))
