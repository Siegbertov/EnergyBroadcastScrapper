import re
import os
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import json
import enum
from datetime import time, datetime, timedelta


UPDATE_EMOJI = "🔄"
DISK_EMOJI = "💾"
CONNECTED_EMOJI = "❤️"
DISCONNECTED_EMOJI = "💔"

NUM_PERIOD = {
    "0":"⁰",
    "1":"¹",
    "2":"²",
    "3":"³",
    "4":"⁴",
    "5":"⁵",
    "6":"⁶",
    "7":"⁷",
    "8":"⁸",
    "9":"⁹"
}

MONTH_UA_OR = {
                            "01":"січня",
                            "02": "лютого",
                            "03":"березня",
                            "04": "квітня",
                            "05":"травня",
                            "06": "червня",
                            "07":"липня",
                            "08": "серпня",
                            "09":"вересня",
                            "10": "жовтня",
                            "11":"листопада",
                            "12": "грудня"
                        }
                        
class MODE(enum.Enum):
    FULL = "FULL"
    ORDER = "ORDER"       
    ORDER_R = "ORDER_R"              

class VIEW(enum.Enum):
    INLINE = "INLINE"
    ON_PAIRS = "ON_PAIRS"
    OFF_PAIRS = "OFF_PAIRS"

class TOTAL(enum.Enum):
    NONE = "NONE"
    ON = "ON"
    OFF = "OFF"

class TG(enum.Enum):
    TRUE = True
    FALSE = False

def re_search_all_off_lines(text:str, pattern_r:str) -> dict:
    result = {}
    try:
        pattern = re.compile(pattern_r)
        matches = pattern.finditer(text)
        for match in matches:
            h1, h2, group = match.group(1), match.group(2), match.group(3)
            if group not in result:
                result[group] = []
            result[group].append(f"{h1}-{h2}")
    except Exception as e:
        pass #TODO exception handling

    for pair in result.keys():
        result[pair].sort()

    result = {k: v for k, v in sorted(list(result.items()))}

    temp = {}
    for pair in result.keys():
        current_inline = "+".join(result[pair])
        if not current_inline.startswith("00:00"):
            current_inline = f"00:00+{current_inline}"
        if not current_inline.endswith("24:00"):
            current_inline = f"{current_inline}+24:00"
        temp[pair] = current_inline

    return temp

def re_search_day_and_month(text:str, pattern_r:str) -> tuple:
    result = (None, None)
    try:
        pattern = re.compile(pattern_r)
        match = pattern.search(text)
        result = (match.group(1), match.group(2))
    except Exception as e:
        pass #TODO exception handling
    return result

def scrapper(link:str, day_month_r:str, group_r:str) -> dict:
    result_d = {}
    temp_d = {}
    try:
       r = requests.get(link)
       soup = BeautifulSoup(r.text, 'html.parser')
       posts = soup.find_all("div", {"class": "tgme_widget_message_bubble"})
       for post in posts:
            text = post.find("div", {"class": "tgme_widget_message_text"})

            if text is not None:
                day, month = re_search_day_and_month(text=text.text, pattern_r=day_month_r)
                groups = re_search_all_off_lines(text=text.text, pattern_r=group_r)
                if not(day is None or month is None or groups == {}):
                    temp_d[f"{day} {month}"] = groups
    except requests.ConnectionError as e:
        pass

    for reversed_key in list(temp_d.keys())[::-1]:
        if reversed_key not in result_d:
            result_d[reversed_key] = temp_d[reversed_key]
    return dict(reversed(list(result_d.items())))

def write_to_json_file(data:dict, filename:str, mode='w'):
    with open(filename, mode, encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def read_from_json_file(filename:str)->dict:
    d = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            d = json.load(file)
    except Exception as e:
        pass
    return d

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def bold(txt:str) -> str:
    return f'**{txt}**'
    
def italic(txt:str) -> str:
    return f'__{txt}__'
    
def mono(txt:str) -> str:
    return f'`{txt}`'
    
def empty() -> str:
    return ''

def difference_in_time(hour_1:list, hour_2:list) -> list:
    d_1 = timedelta(hours=int(hour_1[0]), minutes=int(hour_1[1]))
    d_2 = timedelta(hours=int(hour_2[0]), minutes=int(hour_2[1]))

    result = d_2 - d_1
    H, M, _ = str(result).split(":")
    return [H, M]

def sum_of_time(hour_1:list, hour_2:list) -> list:
    d_1 = timedelta(hours=int(hour_1[0]), minutes=int(hour_1[1]))
    d_2 = timedelta(hours=int(hour_2[0]), minutes=int(hour_2[1]))

    result = d_2 + d_1
    H, M, _ = str(result).split(":")
    return [H, M]

def get_time_period(text:str, period_str=NUM_PERIOD) -> str:
    hs, ms = text.split(":")
    result = ""
    for m in ms:
        result += NUM_PERIOD[m]
    return f"{hs}{result}"

def edit_time_period(text:str) -> str:
    return re.sub(r"(\d\d:\d\d)", lambda x: get_time_period(x.group(1)), text)

def get_current_time() -> str:
    return datetime.now().strftime("%d.%d %H:%M:%S")

if __name__ == "__main__":
    # JSON_FILE = "posts.json"
    # data_d = read_from_json_file(JSON_FILE)
    # for k, v in data_d.items():
    #     print(k, v)

    # print(difference_in_time(('10', '00'), ('12', '50')))
    # print(sum_of_time(('10', '00'), ('12', '50')))
    # TIME = "asdasdasda12:15asdasda15:00sdasd"
    # replacement = re.sub(r"(\d\d:\d\d)", lambda x: get_time_period(x.group(1)), TIME)
    # print(replacement)
    # result = get_time_period("12:15")
    # print(result)

    print(get_current_time())
