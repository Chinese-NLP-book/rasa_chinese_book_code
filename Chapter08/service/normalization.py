import datetime
from typing import Optional


def text_to_date(text_date: str) -> Optional[datetime.date]:
    """convert text based Chinese date info into datatime object

    if the convert is not supprted will return None
    """

    today = datetime.datetime.now()
    one_more_day = datetime.timedelta(days=1)

    if text_date == "今天":
        return today.date()
    if text_date == "明天":
        return (today + one_more_day).date()
    if text_date == "后天":
        return (today + one_more_day * 2).date()

    # Not supported by weather API provider freely
    if text_date == "大后天":
        # return 3
        return (today + one_more_day * 3).date()

    if text_date.startswith("星期"):
        # not supported yet
        return None

    if text_date.startswith("下星期"):
        # not supported yet
        return None

    # follow APIs are not supported by weather API provider freely
    if text_date == "昨天":
        return None
    if text_date == "前天":
        return None
    if text_date == "大前天":
        return None
