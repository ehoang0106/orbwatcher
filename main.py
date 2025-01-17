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
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
import pytz
from decimal import Decimal, InvalidOperation

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


def insert_into_dyanmodb(currency_id, currency_name, price_value, exchange_price_value, date, price_change, percentage_change):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('orbwatcher')
    response = table.put_item(
        Item={
            'currency_id': currency_id,
            'currency_name': currency_name,
            'price_value': price_value,
            'exchange_price_value': exchange_price_value,
            'date': date,
            'price_change': price_change,
            'percentage_change': percentage_change
        }
    )
    return response

def get_previous_price(currency_id):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('orbwatcher')
    
    response = table.query(
        KeyConditionExpression=Key('currency_id').eq(currency_id),
        ScanIndexForward=False,
        Limit=1
    )
    
    if response['Items']:
        return response['Items'][0]['price_value']
    else:
        return None
    

def search_prices(type):
    driver = init_driver()
    url = f"https://orbwatch.trade/#{type}"
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
            currency_id = currency_name_span['data-tooltip-id']
            price_value_span = row.find('span', {'class': 'price-value'})
            if price_value_span:
                price_value = price_value_span.text
                price_arrow_span = price_value_span.find_next('span', {'class': 'price-arrow'})
                if price_arrow_span:
                    exchange_price_value_span = price_arrow_span.find_next('span', {'class': 'price-value'})
                    if exchange_price_value_span:
                        exchange_price_value = exchange_price_value_span.text
                        formatted_currency_name = currency_name.replace(" ", "").replace("'", "").replace("(", "").replace(")", "")
                        
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
                            
                        previous_price = get_previous_price(currency_id)
                        try:
                            if previous_price is not None:
                                previous_price = Decimal(previous_price)
                                price_value = Decimal(price_value)
                                price_change = price_value - previous_price
                                percentage_change = (price_change / previous_price) * 100
                            else:
                                price_change = None
                                percentage_change = None
                        except InvalidOperation:
                            price_change = None
                            percentage_change = None
                        

                        data.append({
                            'currency_id': currency_id,
                            'currency_name': currency_name,
                            'price_value': price_value,
                            'exchange_price_value': exchange_price_value,
                            'formatted_currency_name': formatted_currency_name,
                            'emoji_id': emoji_id,
                            'price_change': price_change,
                            'percentage_change': percentage_change
                        })
                        
                        date = datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%Y-%m-%d %H:%M")
                        #insert data into dynamodb
                        insert_into_dyanmodb(currency_id, currency_name, price_value, exchange_price_value, date, price_change, percentage_change)
                        
    last_update = soup.find('div', {'class': 'timestamp'}).text
    if last_update:
        print(f"{last_update}")
    

    driver.quit()
    
    return data

search_prices('currency')