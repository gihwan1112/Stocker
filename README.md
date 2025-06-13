# Stocker

## 실험 환경

- **Python**: 3.12.8
- **Visual Studio Code**:1.100.3

### 주요 라이브러리 
아래는 프로젝트에서 핵심적으로 사용한 라이브러리입니다.  
전체 목록은 `requirements.txt`를 참고해주세요.

| 라이브러리        | 버전      |
| ----------------- | --------- |
| numpy             | 1.26.4    |
| pandas            | 2.2.3     |
| scikit-learn      | 1.6.1     |
| torch             | 2.7.0     |
| transformers      | 4.52.4    |
| matplotlib        | 3.10.1    |
| tensorflow        | 2.19.0    |
| xgboost           | 3.0.2     |

### 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/gihwan1112/Stocker
cd Stocker

# 2. 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. Jupyter Notebook 실행
jupyter notebook
```
## 파일 및 코드 설명

### newstext_data_crawling.ipynb

- **설명**  
  Daum 뉴스 검색을 이용해 지정된 기간(2023-03-01 ~ 2024-02-29) 동안 ‘삼성전자’ 키워드로 매일 최대 5페이지까지 뉴스 제목을 수집하고, 이를 CSV 파일로 저장

- **주요 라이브러리**  
  `requests`, `beautifulsoup4`, `pandas`

- **주요 기능**  
  1. 검색 키워드(`keyword`), 시작일(`start_date`), 종료일(`end_date`) 설정  
  2. 날짜별(`while date <= end_date`) & 페이지별(`for page in range(1,6)`) URL 생성 및 HTTP 요청  
  3. BeautifulSoup로 HTML 파싱 → 뉴스 제목 추출(`.item-title a`)  
  4. 추출한 데이터를 DataFrame으로 변환 →  
     `daum_news_samsung_20230301_20230229.csv`로 저장

### stockprice_data_crawling.ipynb

- **설명**  
  Naver 금융(네이버 증권) “일별 시세” 페이지를 크롤링해 삼성전자(코드 005930)의 지정 기간(2023-03-01 ~ 2024-02-28) 일별 종가, 거래량, 변동률, 상승 여부를 계산하고 CSV로 저장

- **주요 라이브러리**  
  `requests`, `beautifulsoup4`, `pandas`

- **주요 기능**  
  1. 종목 코드(`code`), 시작일(`start_date`), 종료일(`end_date`) 설정  
  2. 페이지별(`for page in range(1,70)`) HTTP 요청 → HTML 파싱 → `<table class="type2">` 에서 데이터 추출  
  3. 날짜 필터링 → 종가(`cols[1]`), 거래량(`cols[6]`) 수집  
  4. DataFrame 생성 및 중복 제거 → 날짜 순 정렬 → 전일 종가 대비 변동률 계산 → 상승/하락 라벨링(0/1)  
  5. 최종 DataFrame을 `samsung_stock_20230301_20240228.csv`로 저장

