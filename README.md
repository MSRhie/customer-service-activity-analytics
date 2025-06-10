# customer-service-activity-analytics
Python pipeline for preprocessing &amp; feature-engineering Hyundai customer-service call logs (CPI &amp; voice records)

모 대기업 고객센터 CPI 이벤트 로그와 음성 통화 기록을 전처리·통합하여,  
“case 단위”로 정리된 분석용 데이터셋을 생성하는 파이프라인입니다.

---

## 주요 기능

1. **원본 로그 로드**  
   - CSV 형식의 CPI 시스템 로그  
   - XLS 형식의 음성 녹음 시작·종료 기록  

2. **이벤트 매핑 & 필터링**  
   - CPI 이벤트명(`EventAgentReady`, `EventHeld` 등)을 한글(대기, 보류, 보류해제 등)로 일괄 변환  
   - 통화 관련 이벤트(`전화받기`, `전화걸기`, `전화종료`)만 추출  

3. **통화 세션(case_id) 생성**  
   - `database_id + 날짜 + 세션번호` 조합  
   - 벡터화된 `cumsum` 로 “전화걸기·받기” 구간 구분

4. **플래그 & 파생 변수**  
   - 전화받기/걸기 여부 플래그  
   - 장콜(10분 이상) 여부  
   - 상담중/후처리 구분, 대기 전환 전 종료 여부 등  

5. **중복 이벤트 제거**  
   - 연속 중복 액티비티 한 번만 남기기  
   - 세이프티 플래그(`APPNM_safety_flag`)로 안정적 필터링  

---

## 프로젝트 구조
   ```arduino
   customer-service-activity-analytics/
   ├── README.md
   ├── LICENSE # MIT
   ├── requirements.txt
   ├── configs/
   │ └── config.yaml # 데이터 경로·아이디 목록 설정
   ├── data/
   │ ├── raw/ # 원본 CSV·XLS 데이터 (Git 관리 제외)
   │ └── processed/ # 결과물 저장 디렉터리
   ├── src/
   │ ├── init.py
   │ ├── config.py # config.yaml 로딩
   │ ├── data_loader.py # CSV/XLS 읽기
   │ ├── preprocessing.py # 이벤트 매핑·필터링
   │ ├── feature_engineering.py # case_id 생성·플래그 추가·중복 제거
   │ └── main.py # 전체 파이프라인 실행 스크립트
   └── tests/
   ├── test_preprocessing.py
   └── test_feature_engineering.py
   ```

## 설치 및 실행

1. 리포지토리 클론  
      ```bash
      git clone https://github.com/your-id/call-log-pipeline.git
      cd call-log-pipeline
      ```
   
2. 가상환경 생성 & 활성화
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate    # macOS/Linux
      .\.venv\Scripts\activate     # Windows
      ```
   
3. 의존성 설치
     ```bash
     pip install --upgrade pip
     pip install -r requirements.txt
     ```

4. configs/config.yaml 수정
     ```bash
     data_path:
       raw: "./data/raw"
       processed: "./data/processed"
     database_ids:
       - N_R_2_01
       - N_R_2_02
       # …
     ```

5. 파이프라인 실행
      ```bash
      python src/main.py configs/config.yaml
      ```
      * 결과 CSV: data/processed/result_final.csv
   
## 테스트
   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```

## 라이선스
자세한 내용은 LICENSE 파일을 참고하세요.
   
