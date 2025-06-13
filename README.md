# Stocker

## 실험 환경

- **Python**: 3.12.8 

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
