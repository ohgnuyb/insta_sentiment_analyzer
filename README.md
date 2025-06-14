### Instagram 크롤러 & 해시태그 여론 분석 프로젝트

- 참고 자료

[Gobo.log](https://velog.io/@xodbs6/Practice-%EC%9D%B8%EC%8A%A4%ED%83%80-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%B9%B4%EC%B9%B4%EC%98%A4-API-Counter) 님의 게시글을 참고하여 프로젝트를 구현했습니다.

- 프로젝트 개요

본 프로젝트는 Selenium과 DistilBERT 모델을 이용하여 Instagram에서 특정 키워드를 검색하고 게시물의 내용을 수집하여 여론 분석을 수행하는 Python 기반 크롤러입니다.

- 주요 기능

Instagram 로그인: Selenium을 이용하여 사용자의 인스타그램 계정에 로그인합니다.

키워드 검색: 입력받은 키워드를 기반으로 인스타그램에서 해당 키워드와 관련된 게시물을 검색합니다.

게시물 정보 추출: 각 게시물의 내용, 날짜, 해시태그를 추출합니다.

여론 분석: DistilBERT 모델을 이용하여 게시물 내용의 여론 (긍정, 부정, 중립) 을 분석합니다.

결과 출력: 분석 결과를 터미널에 출력하고, 긍정/부정/중립 게시물의 비율을 계산하여 보여줍니다.

- 파일 개요

└── insta_sentiment_analyzer.py           # 메인 Python 스크립트

└── requirements.txt          # 라이브러리 설치 정리

- 사용한 라이브러리 & 모듈 <br>

selenium	4.27.1	웹 스크래핑 및 브라우저 자동화 (Edge 브라우저 제어, 웹 요소 찾기, 특정 상태 기다리기 등)

transformers	4.46.3	자연어 처리 (DistilBERT 모델 사용, 텍스트 분류, 모델 학습 등)

time		표준 라이브러리 (시간 관련 함수 제공)

re		표준 라이브러리 (정규 표현식 사용)

beautifulsoup4	4.12.3	HTML 및 XML 파싱 (웹 스크래핑)

<br>

- 사용 방법

필요한 라이브러리 설치: requirements.txt 파일을 이용하여 필요한 라이브러리를 설치합니다.

Edge 드라이버 설정: `webdriver_manager` 라이브러리를 사용하여 Edge 드라이버가 자동으로 관리됩니다. 별도로 `msedgedriver.exe` 파일을 다운로드하여 프로젝트 폴더에 위치시킬 필요가 없습니다.

스크립트 실행: insta_sentiment_analyzer.py 파일을 실행합니다.

정보 입력: 스크립트 실행 후, 인스타그램 아이디, 비밀번호, 검색 키워드, 검색 게시물 개수를 입력합니다.


- 추가 정보

본 프로젝트는 DistilBERT 모델을 사용하여 여론 분석을 수행합니다. DistilBERT는 BERT 모델을 경량화한 버전으로, 긴 텍스트를 처리하는 데 효과적이며, 빠르고 메모리 효율적으로 동작합니다.

Instagram의 웹 페이지 구조는 변경될 수 있으므로, 코드가 제대로 작동하지 않을 경우 CSS selector를 확인하고 수정해야 할 수 있습니다.

더 정확한 여론 분석을 위해서는 DistilBERT 모델을 fine-tuning하거나, 더 많은 데이터를 사용하여 학습시키는 것이 필요할 수 있습니다.