import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# ChromeDriver 경로 설정
driver_path = "./chromedriver.exe"  # chromedriver.exe 경로
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# 검색어와 폴더 이름 매핑 (나라별로 분류)
search_queries = {
    "japan": {
        # 일본 동전
        "1 yen coin front Japan": "1_yen_coin_japan",
        "5 yen coin front Japan": "5_yen_coin_japan",
        "10 yen coin front Japan": "10_yen_coin_japan",
        "50 yen coin front Japan": "50_yen_coin_japan",
        "100 yen coin front Japan": "100_yen_coin_japan",
        "500 yen coin front Japan": "500_yen_coin_japan",
        # 일본 지폐
        "1000 yen banknote front Japan": "1000_yen_banknote_japan",
        "2000 yen banknote front Japan": "2000_yen_banknote_japan",
        "5000 yen banknote front Japan": "5000_yen_banknote_japan",
        "10000 yen banknote front Japan": "10000_yen_banknote_japan",
    },
    "taiwan": {
        # 대만 동전
        "1 yuan coin front Taiwan": "1_yuan_coin_taiwan",
        "5 yuan coin front Taiwan": "5_yuan_coin_taiwan",
        "10 yuan coin front Taiwan": "10_yuan_coin_taiwan",
        "20 yuan coin front Taiwan": "20_yuan_coin_taiwan",
        "50 yuan coin front Taiwan": "50_yuan_coin_taiwan",
        # 대만 지폐
        "100 yuan banknote front Taiwan": "100_yuan_banknote_taiwan",
        "200 yuan banknote front Taiwan": "200_yuan_banknote_taiwan",
        "500 yuan banknote front Taiwan": "500_yuan_banknote_taiwan",
        "1000 yuan banknote front Taiwan": "1000_yuan_banknote_taiwan",
        "2000 yuan banknote front Taiwan": "2000_yuan_banknote_taiwan",
    },
    "hong_kong": {
        # 홍콩 동전
        "10 cents coin front Hong Kong": "10_cents_coin_hong_kong",
        "20 cents coin front Hong Kong": "20_cents_coin_hong_kong",
        "50 cents coin front Hong Kong": "50_cents_coin_hong_kong",
        "1 dollar coin front Hong Kong": "1_dollar_coin_hong_kong",
        "2 dollars coin front Hong Kong": "2_dollars_coin_hong_kong",
        "5 dollars coin front Hong Kong": "5_dollars_coin_hong_kong",
        "10 dollars coin front Hong Kong": "10_dollars_coin_hong_kong",
        # 홍콩 지폐
        "10 dollars banknote front Hong Kong": "10_dollars_banknote_hong_kong",
        "20 dollars banknote front Hong Kong": "20_dollars_banknote_hong_kong",
        "50 dollars banknote front Hong Kong": "50_dollars_banknote_hong_kong",
        "100 dollars banknote front Hong Kong": "100_dollars_banknote_hong_kong",
        "500 dollars banknote front Hong Kong": "500_dollars_banknote_hong_kong",
        "1000 dollars banknote front Hong Kong": "1000_dollars_banknote_hong_kong",
    },
    "vietnam": {
        # 베트남 동전
        "200 dong coin front Vietnam": "200_dong_coin_vietnam",
        "500 dong coin front Vietnam": "500_dong_coin_vietnam",
        "1000 dong coin front Vietnam": "1000_dong_coin_vietnam",
        "2000 dong coin front Vietnam": "2000_dong_coin_vietnam",
        "5000 dong coin front Vietnam": "5000_dong_coin_vietnam",
        # 베트남 지폐
        "10000 dong banknote front Vietnam": "10000_dong_banknote_vietnam",
        "20000 dong banknote front Vietnam": "20000_dong_banknote_vietnam",
        "50000 dong banknote front Vietnam": "50000_dong_banknote_vietnam",
        "100000 dong banknote front Vietnam": "100000_dong_banknote_vietnam",
        "200000 dong banknote front Vietnam": "200000_dong_banknote_vietnam",
        "500000 dong banknote front Vietnam": "500000_dong_banknote_vietnam",
    },
    "australia": {
        # 호주 동전
        "5 cents coin front Australia": "5_cents_coin_australia",
        "10 cents coin front Australia": "10_cents_coin_australia",
        "20 cents coin front Australia": "20_cents_coin_australia",
        "50 cents coin front Australia": "50_cents_coin_australia",
        "1 dollar coin front Australia": "1_dollar_coin_australia",
        "2 dollars coin front Australia": "2_dollars_coin_australia",
        # 호주 지폐
        "5 dollars banknote front Australia": "5_dollars_banknote_australia",
        "10 dollars banknote front Australia": "10_dollars_banknote_australia",
        "20 dollars banknote front Australia": "20_dollars_banknote_australia",
        "50 dollars banknote front Australia": "50_dollars_banknote_australia",
        "100 dollars banknote front Australia": "100_dollars_banknote_australia",
    }
}

# 기본 저장 폴더 설정
base_dir = "data"  # 최상위 폴더 이름
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# 이미지 수집 시작
for country, queries in search_queries.items():
    # 나라별 폴더 생성
    country_dir = os.path.join(base_dir, country)
    if not os.path.exists(country_dir):
        os.makedirs(country_dir)

    for query, folder_name in queries.items():
        # 화폐별 폴더 생성
        currency_dir = os.path.join(country_dir, folder_name)
        if not os.path.exists(currency_dir):
            os.makedirs(currency_dir)

        # Bing 이미지 검색
        driver.get(f"https://www.bing.com/images/search?q={query}")
        time.sleep(5)  # 페이지 로딩 대기

        # 썸네일 찾기
        thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.mimg")
        print(f"Found {len(thumbnails)} thumbnails for query: {query}")

        # 썸네일 이미지 다운로드 (최대 20개 다운로드)
        for i, thumbnail in enumerate(thumbnails[:25]):  # 최대 20개로 확장
            try:
                # 이미지 URL 가져오기
                src = thumbnail.get_attribute("src")
                if src and src.startswith("http"):  # 유효한 이미지 URL 확인
                    filename = f"{currency_dir}/{folder_name}_{i}.jpg"
                    urllib.request.urlretrieve(src, filename)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Skipping invalid or placeholder image: {src}")
            except Exception as e:
                print(f"Error downloading image {i} for {query}: {e}")

# WebDriver 종료
driver.quit()
