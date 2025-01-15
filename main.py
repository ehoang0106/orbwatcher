from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--remote-debugging-port=0")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def search_exalted():
    driver = init_driver()
    url = "https://orbwatch.trade/"
    driver.get(url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-tooltip-id]'))
    )
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    data = []
    
    rows = soup.find_all('tr')
    for row in rows:
        currency_name_span = row.find('span', {'data-tooltip-id': True})
        if currency_name_span:
            currency_name = currency_name_span.text
            price_value_span = row.find('span', {'class': 'price-value'})
            if price_value_span:
                price_value = price_value_span.text
                price_arrow_span = price_value_span.find_next('span', {'class': 'price-arrow'})
                if price_arrow_span:
                    exchange_price_value_span = price_arrow_span.find_next('span', {'class': 'price-value'})
                    if exchange_price_value_span:
                        exchange_price_value = exchange_price_value_span.text
                        formatted_currency_name = currency_name.replace(" ", "").replace("'", "")
                        
                        #load emoji data from json file
                        with open('emoji.json', 'r') as f:
                            emoji_data = json.load(f)
                        #search for emoji id
                        for emoji in emoji_data:
                            if emoji['emoji_name'] == formatted_currency_name:
                                emoji_id = emoji['emoji_id']
                                break
                        else:
                            emoji_id = None

                        data.append({
                            'currency_name': currency_name,
                            'price_value': price_value,
                            'exchange_price_value': exchange_price_value,
                            'formatted_currency_name': formatted_currency_name,
                            'emoji_id': emoji_id
                        })
    last_update = soup.find('div', {'class': 'timestamp'}).text
    if last_update:
        print(f"{last_update}")
        
    
    
    # for item in data:
    #     print(f"{item['currency_name']}: {item['price_value']} Exalted -> {item['exchange_price_value']} {item['currency_name']}")

    #print(data)
    driver.quit()
    
    return data

