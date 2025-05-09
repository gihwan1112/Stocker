import requests
from bs4 import BeautifulSoup
import pandas as pd

# 삼성전자 코드
code = '005930'
headers = {'User-Agent': 'Mozilla/5.0'}

# 수집할 날짜 범위
target_dates = ['2025.04.21', '2025.04.22', '2025.04.23', '2025.04.24', '2025.04.25']

# 데이터를 저장할 리스트
data = []

# 1~3페이지 돌면서 데이터 수집
for page in range(1, 4):
    url = f"https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    table = soup.find('table', class_='type2')
    rows = table.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 6:
            date = cols[0].get_text(strip=True)
            close_price = cols[1].get_text(strip=True).replace(',', '')
            volume = cols[6].get_text(strip=True).replace(',', '')
            
            if date in target_dates:
                data.append({
                    '날짜': date,
                    '종가': int(close_price),
                    '거래량': int(volume)
                })

# 데이터프레임으로 변환
df = pd.DataFrame(data).drop_duplicates(subset='날짜')
df = df.sort_values('날짜').reset_index(drop=True)

# 전일 종가 추가 (shift 사용)
df['전일종가'] = df['종가'].shift(1)

# 변동률 계산
df['변동률(%)'] = ((df['종가'] - df['전일종가']) / df['전일종가']) * 100
df['변동률(%)'] = df['변동률(%)'].fillna(0)  # 첫 행은 0으로

# 전일종가 컬럼 삭제 (표시 안 하고 싶으면)
df = df.drop(columns=['전일종가'])

# 소수점 둘째자리까지만 반올림
df['변동률(%)'] = df['변동률(%)'].round(2)

# 결과 출력
print(df)

# CSV 저장
df.to_csv('samsung_stock_final.csv', index=False, encoding='utf-8-sig')
