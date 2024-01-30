import streamlit as st
from crawling import AgodaHotelCrawler
from concurrent.futures import ThreadPoolExecutor
import concurrent

def crawl_hotel(url):
    crawler = AgodaHotelCrawler(url)
    return crawler.crawl()

st.title('Agoda Crawling')

# List of URLs
url_skypark = "https://www.agoda.com/ko-kr/hotel-skypark-myeongdong-iii/hotel/seoul-kr.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1555740&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2024-02-3&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=KRW&isFreeOccSearch=false&isCityHaveAsq=false&los=1&searchrequestid=036d4f44-726e-4dbc-8381-7290d27787ec&ds=dEvju4XSkv7GLXKZ"
url_migliore = "https://www.agoda.com/ko-kr/loisir-hotel-seoul-myeongdong/hotel/seoul-kr.html?finalPriceView=1&isShowMobileAppPrice=false&cid=1555740&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2024-02-3&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=KRW&isFreeOccSearch=false&isCityHaveAsq=false&tspTypes=7%2C9&los=1&searchrequestid=036d4f44-726e-4dbc-8381-7290d27787ec&ds=ufDaBef32hQzViDN"

urls = [
    url_skypark, 
    url_migliore
    ]

with ThreadPoolExecutor() as executor:
    # Start the operations and mark each future with its URL
    future_to_url = {executor.submit(crawl_hotel, url): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            hotel_name, hotel_data = future.result()
            st.write(hotel_name)
            st.dataframe(hotel_data)
        except Exception as exc:
            st.write(f'{url} generated an exception: {exc}')
