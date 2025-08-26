"""
Korean Government SSL Adapter

한국 공공데이터 API 서버의 구형 SSL 설정에 맞춘 어댑터
SSL Labs 분석 결과를 기반으로 최적화된 SSL 컨텍스트를 제공합니다.
"""

import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context


class PublicDataApiSSLAdapter(HTTPAdapter):
    """
    한국 공공데이터 API 서버의 구형 SSL 설정에 맞춘 어댑터

    이 어댑터는 다음과 같은 문제를 해결합니다:
    - TLS 1.3 미지원 서버와의 호환성
    - 구형 Cipher Suite 지원
    - SNI (Server Name Indication) 문제
    - 인증서 체인 검증 문제

    Usage:
        adapter = GovernmentSSLAdapter()
        session = adapter.create_government_session()
        response = session.get("https://apis.data.go.kr/your-endpoint")
    """

    def init_poolmanager(self, *args, **kwargs):
        """
        SSL 컨텍스트를 공공데이터 API 서버 스펙에 맞게 초기화

        SSL Labs 분석 결과를 기반으로 다음을 설정:
        - TLS 버전: 1.0, 1.2 (1.3 미지원 서버 대응)
        - Cipher Suite: 구형 암호화 방식 포함
        - 레거시 호환성 옵션
        """
        # SSL 컨텍스트 생성
        ctx = create_urllib3_context()

        # 1. TLS 버전 설정 (서버가 1.0, 1.2만 지원)
        ctx.minimum_version = ssl.TLSVersion.TLSv1  # 서버 호환성을 위해 1.0 허용
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2  # 서버가 1.3 미지원

        # 2. 서버가 지원하는 약한 cipher suite 허용
        # SSL Labs 결과에서 확인된 지원 암호화 방식
        weak_ciphers = [
            "AES128-SHA",  # TLS_RSA_WITH_AES_128_CBC_SHA
            "AES256-SHA",  # TLS_RSA_WITH_AES_256_CBC_SHA
            "DHE-RSA-AES128-SHA",  # TLS_DHE_RSA_WITH_AES_128_CBC_SHA
            "DHE-RSA-AES256-SHA",  # TLS_DHE_RSA_WITH_AES_256_CBC_SHA
            "DES-CBC3-SHA",  # TLS_RSA_WITH_3DES_EDE_CBC_SHA (매우 약함)
        ]

        # 약한 암호화 포함하여 설정 (정부 서버 호환성을 위해)
        cipher_string = ":".join(weak_ciphers) + ":!aNULL:!eNULL"
        ctx.set_ciphers(cipher_string)

        # 3. 추가 호환성 옵션들
        ctx.check_hostname = False  # SNI 문제 해결
        ctx.verify_mode = ssl.CERT_NONE  # 인증서 검증 우회 (필요시)

        # 4. 레거시 호환성 옵션
        ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT
        if hasattr(ssl, "OP_DONT_INSERT_EMPTY_FRAGMENTS"):
            ctx.options |= ssl.OP_DONT_INSERT_EMPTY_FRAGMENTS

        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)

    def create_public_data_api_session(self):
        """
        공공데이터 API용 최적화된 requests 세션 생성

        Returns:
            requests.Session: 공공데이터 API 호출에 최적화된 세션

        Example:
            >>> adapter = PublicDataApiSSLAdapter()
            >>> session = adapter.create_public_data_api_session()
            >>> response = session.get("https://apis.data.go.kr/endpoint")
        """
        session = requests.Session()

        # SSL 어댑터 적용
        session.mount("https://", PublicDataApiSSLAdapter())

        # 헤더 설정 (일부 공공데이터 사이트에서 요구)
        session.headers.clear()
        session.headers.update(
            {
                "User-Agent": ("User-Agent"),
                "Accept": "application/json, application/xml, text/plain, */*",
                "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.data.go.kr",
            }
        )

        return session


# 편의를 위한 팩토리 함수들
def create_public_data_api_session():
    """
    공공데이터 API용 세션을 빠르게 생성하는 편의 함수

    Returns:
        requests.Session: 공공데이터 API 호출용 세션

    Example:
        >>> session = create_public_data_api_session()
        >>> response = session.get("https://apis.data.go.kr/endpoint")
    """
    adapter = PublicDataApiSSLAdapter()
    return adapter.create_public_data_api_session()


def public_data_api_get(url, **kwargs):
    """
    공공데이터 API에 GET 요청을 보내는 편의 함수

    Args:
        url (str): 요청할 URL
        **kwargs: requests.get()에 전달할 추가 인자들

    Returns:
        requests.Response: API 응답

    Example:
        >>> response = public_data_api_get("https://apis.data.go.kr/endpoint")
        >>> print(response.json())
    """
    session = create_public_data_api_session()
    return session.get(url, **kwargs)


def public_data_api_post(url, **kwargs):
    """
    공공데이터 API에 POST 요청을 보내는 편의 함수

    Args:
        url (str): 요청할 URL
        **kwargs: requests.post()에 전달할 추가 인자들

    Returns:
        requests.Response: API 응답

    Example:
        >>> response = public_data_api_post("https://apis.data.go.kr/endpoint",
        ...                          json={"key": "value"})
    """
    session = create_public_data_api_session()
    return session.post(url, **kwargs)


if __name__ == "__main__":
    # 간단한 테스트
    print("Korean Government SSL Adapter")
    print("============================")

    try:
        session = create_public_data_api_session()
        print("✅ SSL 어댑터 세션 생성 성공")

        # 실제 테스트를 원한다면 아래 주석을 해제하고 유효한 API URL을 입력하세요
        # response = session.get("https://apis.data.go.kr/test-endpoint")
        # print(f"✅ API 호출 성공: {response.status_code}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
