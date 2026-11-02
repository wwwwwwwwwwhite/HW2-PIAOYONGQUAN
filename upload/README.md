# BuildMyPC

BuildMyPC는 사용자의 예산과 컴퓨터 사용 목적을 바탕으로 데스크톱 PC 구성을 추천하는 한국어 웹 서비스입니다.

## 주요 기능

- 예산, 사용 목적, 해상도 입력
- CPU 및 GPU 제조사 선호 선택
- RAM과 저장장치 용량 선택
- CPU, 쿨러, 메인보드, RAM, GPU, SSD, 파워, 케이스 추천
- 모니터와 키보드·마우스 선택 구성
- 부품별 참고 가격, 총액, 예산 잔액 표시
- CPU 소켓, RAM 규격, GPU 길이, 쿨러 높이, 파워 용량 호환성 검사
- 견적 텍스트 복사 및 CSV 다운로드
- FastAPI API와 규칙 기반 추천 로직

## 사용 기술

- Python 3.9 이상
- FastAPI
- Uvicorn
- Pydantic
- HTML, CSS, Vanilla JavaScript
- pytest, FastAPI TestClient

## 설치 환경

Python 3.9 이상과 pip가 필요합니다. 운영체제에서 Python을 설치한 후 터미널에서 `python3 --version`과 `pip --version`으로 확인하세요.

## 설치 방법

프로젝트 루트(`upload`)에서 가상환경을 만들고 의존성을 설치합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 모델 및 환경변수

이 버전은 외부 AI 모델이나 별도 모델 파일을 사용하지 않습니다. 제품 데이터는 `app/data/products.json`에 포함되어 있습니다.

외부 API, 환경변수, API 키도 사용하지 않습니다. 따라서 별도의 `.env` 파일이나 비밀값 설정이 필요하지 않습니다.

## 로컬 실행

`upload` 디렉터리에서 다음 명령을 실행합니다.

```bash
uvicorn app.main:app --reload
```

브라우저에서 [http://127.0.0.1:8000](http://127.0.0.1:8000)을 엽니다. API 문서는 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)에서 확인할 수 있습니다.

## 테스트

가상환경을 활성화한 상태에서 실행합니다.

```bash
pytest -q
```

테스트는 입력값 검증, 추천 결과와 가격 합계, 메인 페이지, health endpoint, 주변기기, 호환성 검사, 부족한 저장장치 데이터 경고를 확인합니다.

## 제품 데이터와 제한사항

`app/data/products.json`의 제품 사양과 가격은 기능 시연을 위한 수동 관리 참고 데이터입니다. 실시간 판매 가격, 재고, 판매처 API와 연동되지 않습니다. 구매 전 실제 판매처에서 가격과 호환성을 다시 확인해야 합니다.

제품 사진을 다운로드하거나 재배포하지 않으며, 현재 화면에는 제품 이미지가 없음을 알리는 대체 영역이 표시됩니다. 제품 이미지와 실시간 가격 API는 추후 사용 허가와 공식 연동 방법을 확인한 뒤 추가해야 합니다.

## 배포 설정

`render.yaml`은 Render에서 사용할 수 있는 설정 예시입니다. GitHub 저장소와 Render 계정을 연결한 후 Blueprint로 적용하고, 배포 뒤 `/health`가 정상 응답하는지 확인해야 합니다. 이 업로드 묶음 자체에는 공개 URL이나 인증정보를 포함하지 않습니다.
