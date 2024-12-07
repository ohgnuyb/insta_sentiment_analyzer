from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transformers import LongformerTokenizer, LongformerForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import torch
import time
import re
from bs4 import BeautifulSoup
import torch

# Edge driver path setup
edge_driver_path = "./msedgedriver.exe" 
edge_options = Options()
edge_options.add_experimental_option("detach", True)
edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

def insta_login(driver, username, password):
    """인스타그램 로그인 함수"""
    driver.get('https://instagram.com')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))

    login_id = driver.find_element(By.NAME, 'username')
    login_id.send_keys(username)
    login_pwd = driver.find_element(By.NAME, 'password')
    login_pwd.send_keys(password)
    login_pwd.submit()

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="button"]')))
        print("로그인 성공!")
    except Exception as e:
        print(f"로그인 오류: {e}")

def go_to_home(driver):
    """인스타그램 홈페이지로 이동하는 함수"""
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="홈"]')))
        print("로그인 상태 확인 완료.")
    except Exception as e:
        print(f"홈 페이지로 이동 중 오류 발생: {e}") 

def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + word
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._aagu')))
    return url

def select_first(driver):
    first = driver.find_element(By.CSS_SELECTOR, 'div._aagu')
    first.click()
    time.sleep(5)

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try: 
       content_with_hashtags = soup.select('div._a9zs')[0].text
       content = re.sub(r'#\S+', '', content_with_hashtags)
    except: 
        content = ' '
    
    tags = re.findall(r'#[^\s#,\\]+', content_with_hashtags)
    if not tags:
        tags = [f"#{keyword}"]
    date = soup.select('time.x1p4m5qa')[0]['datetime'][:10]
    return [content, date, tags]

def move_next(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._aaqg._aaqh button._abl-')))
        right = driver.find_element(By.CSS_SELECTOR, 'div._aaqg._aaqh button._abl-')
        right.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._a9zs')))
    except Exception as e:
        time.sleep(5)

def crawl_instagram(username, password, keyword, num_posts=10):
    try:
        insta_login(driver, username, password)
        go_to_home(driver)

        url = insta_searching(keyword)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._aagu')))
        select_first(driver)

        results = []
        analyzed_count = 0

        while analyzed_count < num_posts:
            try:
                data = get_content(driver)
                results.append(data)
                move_next(driver)
                analyzed_count += 1
            except Exception as e:
                print(f"오류 발생: {e}")
                time.sleep(5)
                move_next(driver)

        return results

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return []

