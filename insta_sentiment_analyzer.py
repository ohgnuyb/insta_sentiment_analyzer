from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import re
from bs4 import BeautifulSoup
from transformers import pipeline
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification



tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

# 감정 분석 파이프라인 설정
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def analyze_sentiment(text):
    # 텍스트에 대한 감정 분석 (truncation=True 옵션 추가)
    # 이 옵션이 텍스트가 모델의 최대 길이보다 길 경우 자동으로 잘라줍니다.
    result = classifier(text, truncation=True)[0]
    
    sentiment = result['label']
    if sentiment == 'POSITIVE':
        return 'POSITIVE'
    elif sentiment == 'NEGATIVE':
        return 'NEGATIVE'
    else:
        return 'NEUTRAL'


    
def print_results(results):
    print("-----------------------------------------------")

    print(f" - 해시태그 게시물 분석:")
    
    sentiment_counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
    seen_posts = set()

    for idx, result in enumerate(results, 1):
        content, date, tags = result

        post_key = (content, date, tuple(tags))
        if post_key in seen_posts:
            continue
        seen_posts.add(post_key)

        sentiment = analyze_sentiment(content)

        print(f"게시물 {idx}:")
        print(f"내용: {content}")
        print(f"날짜: {date}")
        print(f"해시태그: {tags}")
        print(f"내용 여론 분석: {sentiment}\n")

        sentiment_counts[sentiment] += 1

    total_posts = len(seen_posts)
    if total_posts > 0:
        positive_ratio = sentiment_counts['POSITIVE'] / total_posts * 100
        negative_ratio = sentiment_counts['NEGATIVE'] / total_posts * 100
        neutral_ratio = sentiment_counts['NEUTRAL'] / total_posts * 100
        print(f"기능1: 전체 게시물에 대한 여론 분석 결과:")
        print(f"긍정적 비율: {positive_ratio:.2f}%")
        print(f"부정적 비율: {negative_ratio:.2f}%")
        print(f"중립적 비율: {neutral_ratio:.2f}%")
    else:
        print("수집된 게시물이 없습니다.")

# Edge driver path setup
# edge_driver_path = "./msedgedriver.exe"
edge_options = Options()
# edge_options.add_experimental_option("detach", True)
# edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

def insta_login(driver, username, password):
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
        # 내용과 날짜를 가져오는 선택자(selector)를 새 클래스 이름으로 업데이트했습니다.
        
        # 🔻 [수정됨] 내용 부분 클래스 적용
        #_ap3a _aaco _aacu _aacx _aad7 _aade -> ._ap3a._aaco._aacu._aacx._aad7._aade
        content_with_hashtags = soup.select_one('._ap3a._aaco._aacu._aacx._aad7._aade').text
        
        # 🔻 [수정됨] 시간 부분 클래스 적용
        #_a9ze _a9zf -> time._a9ze._a9zf
        date = soup.select_one('time._a9ze._a9zf')['datetime'][:10]

        # 해시태그를 제외한 순수 내용을 추출합니다.
        content = re.sub(r'#\S+', '', content_with_hashtags).strip()
        
        # 해시태그만 따로 추출합니다.
        tags = re.findall(r'#[^\s#,\\]+', content_with_hashtags)

        # 모든 정보가 성공적으로 수집되면 리스트로 반환합니다.
        return [content, date, tags]

    except Exception as e:
        # try 블록 안에서 뭐든 하나라도 실패하면...
        print(f"❗ 게시물 내용 수집 실패 (건너뜁니다): {e}")
        # 프로그램이 멈추지 않도록 빈 데이터를 반환합니다.
        return ['', '날짜 없음', []]
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

# Main execution
if __name__ == "__main__":
    username = input("인스타 아이디 입력:")
    password = input("인스타 비밀번호 입력:")
    keyword = input("검색 키워드 입력:")
    num_posts = int(input("검색 게시물 개수 입력:"))

    try:
        results = crawl_instagram(username, password, keyword, num_posts)
        print("-----------------------------------------------")
        print(f"수집된 게시물 {len(results)}개")
        print_results(results)
    finally:
        driver.quit()