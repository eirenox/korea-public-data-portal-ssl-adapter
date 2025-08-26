#!/usr/bin/env python3
"""
Public Data API SSL Adapter - 사용 예제

이 파일은 public_data_api_ssl_adapter의 다양한 사용 방법을 보여줍니다.
실제 API 호출을 하려면 유효한 API 키와 엔드포인트가 필요합니다.
"""

import os
from public_data_api_ssl_adapter import (
    PublicDataApiSSLAdapter,
    create_public_data_api_session,
    public_data_api_get,
    public_data_api_post,
)


def example_1_basic_usage():
    """예제 1: 기본 사용법"""
    print("=" * 50)
    print("예제 1: 기본 사용법")
    print("=" * 50)

    # 방법 1: 클래스 직접 사용
    adapter = PublicDataApiSSLAdapter()
    session = adapter.create_public_data_api_session()

    print("✅ SSL 어댑터 세션 생성 완료")
    print(f"   - User-Agent: {session.headers.get('User-Agent')}")
    print(f"   - Accept: {session.headers.get('Accept')}")

    # 실제 API 호출 예제 (주석 처리됨)
    # response = session.get("https://apis.data.go.kr/your-endpoint")
    # print(f"   - 응답 코드: {response.status_code}")


def example_2_convenience_functions():
    """예제 2: 편의 함수 사용"""
    print("\n" + "=" * 50)
    print("예제 2: 편의 함수 사용")
    print("=" * 50)

    # 방법 2: 편의 함수 사용
    session = create_public_data_api_session()
    print("✅ 편의 함수로 세션 생성 완료")

    # 또는 직접 GET/POST 함수 사용
    try:
        # 실제 사용시에는 유효한 URL을 입력하세요
        # response = public_data_api_get("https://apis.data.go.kr/test-endpoint")
        # print(f"✅ GET 요청 성공: {response.status_code}")
        print("✅ public_data_api_get 함수 준비 완료")

        # POST 요청 예제
        # response = public_data_api_post("https://apis.data.go.kr/test-endpoint",
        #                          json={"key": "value"})
        print("✅ public_data_api_post 함수 준비 완료")

    except Exception as e:
        print(f"❌ 요청 실패: {e}")


def example_3_real_api_call():
    """예제 3: 실제 API 호출 (공공데이터 포털 예제)"""
    print("\n" + "=" * 50)
    print("예제 3: 실제 API 호출 예제")
    print("=" * 50)

    # 환경변수에서 API 키 읽기
    api_key = os.getenv("DATA_GO_KR_API_KEY")

    if not api_key:
        print("⚠️  DATA_GO_KR_API_KEY 환경변수가 설정되지 않았습니다.")
        print("   실제 API 호출을 원한다면 다음과 같이 설정하세요:")
        print("   export DATA_GO_KR_API_KEY='your-api-key'")
        return

    # 실제 API 호출 예제
    """
    try:
        session = create_public_data_api_session()
        
        url = "https://a.b.c/d"
        
        response = session.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API 호출 성공!")
            print(f"   - 응답 코드: {response.status_code}")
            print(f"   - 데이터 크기: {len(response.text)} bytes")
            
            # JSON 응답 예쁘게 출력
            print("   - 응답 데이터 (첫 500자):")
            print(f"     {response.text[:500]}...")
            
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    """


def example_4_error_handling():
    """예제 4: 에러 처리"""
    print("\n" + "=" * 50)
    print("예제 4: 에러 처리")
    print("=" * 50)

    session = create_public_data_api_session()

    # 잘못된 URL로 테스트
    test_urls = [
        "https://non-existent-api.example.com",
        "https://httpstat.us/500",  # 500 에러 반환
        "https://httpstat.us/404",  # 404 에러 반환
    ]

    for url in test_urls:
        try:
            print(f"\n🔍 테스트 URL: {url}")
            response = session.get(url, timeout=5)
            print(f"✅ 응답: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("❌ 연결 오류: 서버에 연결할 수 없습니다")
        except requests.exceptions.Timeout:
            print("❌ 타임아웃: 요청 시간이 초과되었습니다")
        except requests.exceptions.SSLError as e:
            print(f"❌ SSL 오류: {e}")
        except Exception as e:
            print(f"❌ 기타 오류: {e}")


def example_5_session_reuse():
    """예제 5: 세션 재사용 (성능 최적화)"""
    print("\n" + "=" * 50)
    print("예제 5: 세션 재사용")
    print("=" * 50)

    # 세션을 한 번만 생성하고 재사용
    session = create_public_data_api_session()

    # 여러 번 API 호출할 때 세션 재사용
    urls = [
        "https://httpstat.us/200",
        "https://httpstat.us/201",
        "https://httpstat.us/202",
    ]

    print("🚀 동일한 세션으로 여러 번 요청...")

    for i, url in enumerate(urls, 1):
        try:
            response = session.get(url, timeout=5)
            print(f"   {i}. {url} → {response.status_code}")
        except Exception as e:
            print(f"   {i}. {url} → 오류: {e}")

    print("✅ 세션 재사용 완료 (연결 풀링으로 성능 향상)")


def main():
    """메인 함수 - 모든 예제 실행"""
    print("Public Data API SSL Adapter - 사용 예제")
    print("=" * 60)

    # 모든 예제 실행
    example_1_basic_usage()
    example_2_convenience_functions()
    example_3_real_api_call()
    example_4_error_handling()
    example_5_session_reuse()

    print("\n" + "=" * 60)
    print("🎉 모든 예제 실행 완료!")
    print("💡 실제 API 호출을 위해서는 코드를 수정하여 사용하세요.")
    print("📚 자세한 내용은 README.md를 참고하세요.")


if __name__ == "__main__":
    import requests  # 에러 처리 예제에서 사용

    main()
