# Public Data API SSL Adapter

한국 공공데이터 API의 구형 SSL 설정과 호환되는 Python SSL 어댑터

## 🚨 문제 상황

한국 공공데이터 API를 사용할 때 다음과 같은 SSL 오류가 발생하는 경우가 있습니다:

```python
HTTPSConnectionPool(host='apis.data.go.kr', port=443): 
    Max retries exceeded with url: /... 
        (Caused by SSLError(
            SSLError(1, '[SSL: SSLV3_ALERT_ILLEGAL_PARAMETER] ssl/tls alert illegal parameter (_ssl.c:1020)')))
```

## ❌ 잘못된 해결책들

인터넷에서 흔히 찾을 수 있는 해결책들의 문제점:

```python
# 보안을 완전히 포기하는 방법들
response = requests.get(url, verify=False)  # SSL 검증 비활성화
url = "http://apis.data.go.kr/..."          # HTTP 사용
```

이런 방법들은 **보안 취약점**을 만들고 **중간자 공격**에 노출시킵니다.

## ✅ 올바른 해결책

### 1. SSL Labs 분석

[SSL Labs](https://www.ssllabs.com/)를 사용해서 서버의 SSL 설정을 분석합니다:

- 지원 TLS 버전 확인
- Cipher Suite 목록 분석
- SNI 지원 여부 확인

### 2. 커스텀 SSL 어댑터 사용

서버 스펙에 맞춘 SSL 어댑터로 **보안을 유지하면서** 호환성을 확보합니다.

## 🚀 사용법

### 설치

```bash
pip install requests urllib3
```

### 기본 사용법

```python
from government_ssl_adapter import GovernmentSSLAdapter

# SSL 어댑터 생성
adapter = GovernmentSSLAdapter()
session = adapter.create_government_session()

# 안전한 API 호출
response = session.get("https://apis.data.go.kr/your-api-endpoint")
print(response.status_code)  # 200 OK!
```

### 상세 예제

자세한 사용 예제는 [`example.py`](./example.py)를 참고하세요.

## 📁 파일 구성

```
korean-government-ssl-adapter/
├── README.md                    # 이 파일
├── public_data_api_ssl_adapter.py    # 메인 SSL 어댑터
├── example.py                   # 사용 예제
├── requirements.txt             # 의존성 패키지
└── LICENSE                      # MIT 라이선스
```

## 🔧 어댑터 기능

- **TLS 버전 호환성**: 구형 서버가 지원하는 TLS 1.0/1.2에 맞춤
- **Cipher Suite 최적화**: 서버가 지원하는 암호화 방식 사용
- **SNI 문제 해결**: 가상 호스팅 환경 대응
- **헤더 최적화**: 정부 API에 맞는 요청 헤더 설정

## 🛡️ 보안 고려사항

이 어댑터는 다음과 같은 보안 원칙을 따릅니다:

- ✅ **암호화 연결 유지**: HTTPS 통신 보장
- ✅ **호환성 확보**: 구형 서버와의 연결 가능
- ✅ **근본적 해결**: 임시방편이 아닌 정확한 설정
- ❌ **verify=False 사용 안함**: SSL 검증 우회하지 않음

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [`LICENSE`](./LICENSE) 파일을 참고하세요.

## 📚 관련 글

- [한국 공공데이터 API SSL 연결 문제 해결 블로그 포스트](https://your-blog-link.com)
- [SSL Labs를 활용한 SSL 분석 방법](https://www.ssllabs.com/)

## ⚠️ 주의사항

- 이 어댑터는 구형 SSL 설정을 사용하는 서버와의 호환성을 위해 만들어졌습니다
- 최신 보안 표준을 지원하는 서버에는 기본 SSL 설정 사용을 권장합니다
- 프로덕션 환경에서는 충분한 테스트 후 사용하세요
