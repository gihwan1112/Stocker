# Stocker

## 프로젝트 개요

Stocker는 **뉴스 감성 분석**과 **주가 시계열 데이터**를 결합하여 삼성전자의 일별 주가 변동을 예측·분석하는 파이프라인 프로젝트입니다.  

### 주요 목표
- **시장 심리 지표화**: Daum 뉴스 제목을 KR-FinBERT로 감성 점수화하여 일별 평균 감성 지표 도출  
- **주가 변동 분석**: Naver 금융에서 일별 종가·거래량·변동률·상승 여부를 수집·정리  
- **상관관계 탐색**: 감성 점수와 주가 지표 간 Pearson 상관계수 및 회귀 분석  
- **예측 모델링**: 전일 감성점수·전일 상승 여부·5일 이동평균·거래량 변화율을 특징으로 삼아 RandomForest, GradientBoosting, XGBoost 모델 학습  

### 결과 요약
- **감성 vs 변동률 상관계수**: 0.166
- **최고 성능 모델 (RandomForest Regressor)**: MSE ≈ 2.0703, R² ≈ -0.1220

프로젝트 전 과정을 통해 “뉴스 감성이 실제 주가 변동에 얼마나 영향을 미치는지”를 탐색하고, 간단한 머신러닝 모델로 예측 가능성을 검증했습니다.  

## 실험 환경

- **Python**: 3.12.8
- **Visual Studio Code**:1.100.3

### 주요 라이브러리 
아래는 프로젝트에서 핵심적으로 사용한 라이브러리입니다.  
전체 목록은 `requirements.txt`를 참고해주세요.

| 라이브러리        | 버전      |
| ----------------- | --------- |
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

### preprocessing.ipynb

- **설명**  
  크롤링한 뉴스 제목과 주가 데이터를 불러와 텍스트 전처리 → KR-FinBERT 감성 분석 → 일별 평균 감성 점수 계산 → 주가 데이터와 병합해 최종 전처리된 CSV(`data_preprocessing.csv`)를 생성

- **주요 라이브러리**  
  `pandas`, `re`, `torch`, `transformers`, `tqdm`

- **주요 기능**  
  1. **데이터 로드**  
     - 뉴스: `daum_news_samsung_20230301_20240229.csv`  
     - 주가: `samsung_stock_20230301_20240228.csv`  
  2. **텍스트 정제**  
     - 정규표현식(`clean_text`)으로 특수문자 제거 및 공백 정리 → `clean_title` 컬럼 생성  
  3. **KR-FinBERT 로드 및 감성 분석**  
     - `snunlp/KR-FinBERT-SC` 모델 불러오기  
     - `predict_sentiment` 함수로 각 뉴스 제목별 확률 기반 긍·부정 점수 산출 → `sentiment_score` 컬럼 생성  
  4. **일별 평균 감성 점수 계산**  
     - `daily_sentiment = df.groupby('날짜').avg_sentiment`로 일별 평균 감성 점수 계산 
  5. **주가 데이터 전처리**  
     - 결측치 및 거래량 0 제거  
     - 날짜 정렬 및 형식 통일  
  6. **데이터 병합**  
     - 날짜 기준 내부 조인(inner join) → 주가 정보 + `감성 점수` 컬럼 포함  
     - 컬럼명 정리 및 결측치 채우기(0)  
  7. **최종 저장**  
     - `data_preprocessing.csv` 생성

### visualization.ipynb

- **설명**  
  전처리된 `data_preprocessing.csv`를 불러와, 일별 주가 변동률·상승 여부·감성 점수를 시계열 플롯으로 시각화하고, 감성 점수와 주가 지표 간의 상관관계 및 산점도(선형·2차 회귀선 포함)를 시각화

- **주요 라이브러리**  
  `pandas`, `numpy`, `matplotlib`, `sklearn.metrics`

- **주요 기능**  
  1. **데이터 로드**  
     ```python
     df = pd.read_csv("data/data_preprocessing.csv", parse_dates=['날짜'])
     ```  
  2. **시계열 시각화 (3행 1열 서브플롯)**  
     - **1행:** 일별 주가 변동률(line plot)  
     - **2행:** 일별 상승 여부(bar plot, 0→-1)  
     - **3행:** 일별 평균 감성 점수(line plot)  

  3. **상관관계 분석 출력**  
     ```python
     corr1 = df['상승 여부'].corr(df['감성점수'])
     corr2 = df['감성점수'].corr(df['변동률(%)'])
     print(f"상관계수: {corr1:.3f}, {corr2:.3f}")
     ```

  5. **산점도 및 회귀선 그리기**  
     - 감성 점수 vs. 변동률 산점도  
     - 1차(선형) 회귀선, 2차(비선형) 회귀곡선 추가  

### feature_engineering&modeling.ipynb

- **설명**  
  전처리된 데이터(`data_preprocessing.csv`)를 불러와  
  1) 피처 엔지니어링(전일 감성점수, 전일 상승여부, 5일 이동평균, 거래량 변화율)  
  2) 시계열 분할(train/test)  
  3) RandomForest, GradientBoosting, XGBoost 모델 학습 및 평가(MSE, R²)  
  과정 수행

- **주요 라이브러리**  
  `pandas`, `numpy`, `scikit-learn`, `xgboost`

- **주요 단계**  
  1. `data_preprocessing.csv` 로드 및 날짜 정렬  
  2. 피처 생성  
     ```python
     df["전일_감성점수"]   = df["감성점수"].shift(1)
     df["전일_변동률"]     = df["변동률(%)"].shift(1)
     df["전일_상승여부"]   = df["상승 여부"].shift(1)       
     df["5일_이동평균"]    = df["종가"].rolling(window=5).mean().shift(1)
     df["거래량_변화율"]   = df["거래량"].pct_change().shift(1).round(3)
     ```  
  3. 결측치 제거(`df.dropna()`)  
  4. `train_test_split(..., shuffle=False)`로 시계열 분할  
  5. 모델 정의 및 학습/예측/평가  
     ```python
     models = {
       "RandomForest": RandomForestRegressor(...),
       "GradientBoosting": GradientBoostingRegressor(...),
       "XGBoost": XGBRegressor(...)
     }
     ```  
  6. MSE, R² 결과 출력

## Data

### 1. daum_news_samsung_20230301_20240229.csv
- **설명**:  
  Daum 뉴스 검색(‘삼성전자’)으로 수집한 날짜별 뉴스 제목
- **기간**: 2023-03-01 ~ 2024-02-29  
- **컬럼**:  
  | 컬럼명       | 설명                    | 예시           |
  |-------------|-------------------------|---------------|
  | 날짜        | 뉴스 게시 날짜 (YYYY-MM-DD) | 2023-03-01    |
  | 뉴스제목    | 원본 제목 문자열         | “삼성전자, 1Q 실적 발표” |

### 2. samsung_stock_20230301_20240228.csv
- **설명**:  
  Naver 금융 “일별 시세”에서 크롤링한 삼성전자 주가  
- **기간**: 2023-03-01 ~ 2024-02-28  
- **컬럼**:  
  | 컬럼명      | 설명                           | 예시        |
  |------------|-------------------------------|------------|
  | 날짜       | 거래일 (YYYY.MM.DD)           | 2023.03.01 |
  | 종가       | 당일 종가 (원)                | 75,000     |
  | 거래량     | 당일 거래량                   | 10,234,567 |
  | 변동률(%)  | 전일 대비 등락률 (%)            | 1.23       |
  | 상승 여부  | 상승(1) / 하락(0)              | 1          |

### 3. data_preprocessing.csv
- **설명**:  
  뉴스 감성 점수와 주가 데이터를 날짜 기준으로 병합·정리한 최종 전처리 파일  
- **컬럼**:  
  | 컬럼명       | 설명                                     |
  |-------------|-----------------------------------------|
  | 날짜        | 거래일 (YYYY-MM-DD)                      |
  | 종가        | 당일 종가 (원)                          |
  | 거래량      | 당일 거래량                             |
  | 변동률(%)   | 전일 대비 등락률 (%)                     |
  | 상승 여부   | 상승(1) / 하락(0)                        |
  | 감성점수    | 일별 평균 뉴스 감성 점수 (–1 ~ +1 범위)    |

> **Tip**: 폴더 구조 예시  
> ```
> data/
> ├─ daum_news_samsung_20230301_20240229.csv
> ├─ samsung_stock_20230301_20240228.csv
> └─ data_preprocessing.csv
> ```

