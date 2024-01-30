from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import json


class AgodaHotelCrawler:
    def __init__(self, url):
        self.url = url
        self.hotel_name, self.hotel_data = self.crawl()

    @staticmethod
    def parse_room_info(text):
        pattern = r'(.+?)\s*\(([^)]+)\)([\d\.]+)'
        matches = re.findall(pattern, text)
        room_info = []

        for match in matches:
            room_name, bed_info, rating = match
            room_data = {
                'room_name': room_name.strip(),
                'bed_info': bed_info.strip(),
                'rating': rating
            }
            room_info.append(room_data)

        return json.dumps(room_info, ensure_ascii=False)

    @staticmethod
    def extract_one_night_rate(text):
        matches = re.findall(r'₩\s*(\d+(?:,\d+)*)\s*1박당\s*요금', text)
        return int(matches[0].replace(',', '')) if matches else None

    def crawl(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        with webdriver.Chrome(options=options) as driver:
            driver.get(self.url)
            time.sleep(3)  # Waiting for page to load
            html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")
        hotel_name = soup.find("p", {"class": "HeaderCerebrum__Name"}).text
        room_table = soup.find_all("div", {"class": "MasterRoom"})

        df = pd.DataFrame(columns=["room_price", "room_name", "room_service"])
        for room in room_table:
            room_name = room.find("div", {"class": "MasterRoom-header"}).text
            room_service = room.find("div", {"class": "ChildRoomsList-room-featurebuckets"}).text
            room_price = room.find("div", {"class": "ChildRoom__PriceContainer"}).text

            room_price = self.extract_one_night_rate(room_price)
            df.loc[len(df)] = [room_price, room_name, room_service]
        return hotel_name, df
