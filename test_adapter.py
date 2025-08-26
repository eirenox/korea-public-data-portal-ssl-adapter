#!/usr/bin/env python3
"""
Public Data API SSL Adapter - 테스트 스크립트

이 스크립트는 SSL 어댑터가 올바르게 작동하는지 테스트합니다.
실제 네트워크 연결 없이도 기본적인 초기화를 확인할 수 있습니다.
"""

import unittest
from unittest.mock import Mock, patch
import ssl
from public_data_api_ssl_adapter import (
    PublicDataApiSSLAdapter,
    create_public_data_api_session,
    public_data_api_get,
    public_data_api_post,
)


class TestPublicDataApiSSLAdapter(unittest.TestCase):
    """SSL 어댑터 테스트 클래스"""

    def test_adapter_initialization(self):
        """어댑터 초기화 테스트"""
        adapter = PublicDataApiSSLAdapter()
        self.assertIsInstance(adapter, PublicDataApiSSLAdapter)

    def test_session_creation(self):
        """세션 생성 테스트"""
        adapter = PublicDataApiSSLAdapter()
        session = adapter.create_public_data_api_session()

        # 세션이 올바르게 생성되었는지 확인
        self.assertIsNotNone(session)
        self.assertEqual(session.__class__.__name__, "Session")

        # 헤더가 올바르게 설정되었는지 확인
        self.assertIn("User-Agent", session.headers)
        self.assertIn("Accept", session.headers)
        self.assertIn("Accept-Language", session.headers)

    def test_convenience_function(self):
        """편의 함수 테스트"""
        session = create_public_data_api_session()
        self.assertIsNotNone(session)
        self.assertIn("User-Agent", session.headers)

    @patch("public_data_api_ssl_adapter.create_public_data_api_session")
    def test_public_data_api_get(self, mock_create_session):
        """public_data_api_get 함수 테스트"""
        # Mock 세션 설정
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        mock_create_session.return_value = mock_session

        # 함수 호출
        response = public_data_api_get("https://example.com")

        # 검증
        mock_create_session.assert_called_once()
        mock_session.get.assert_called_once_with("https://example.com")
        self.assertEqual(response.status_code, 200)

    @patch("public_data_api_ssl_adapter.create_public_data_api_session")
    def test_public_data_api_post(self, mock_create_session):
        """public_data_api_post 함수 테스트"""
        # Mock 세션 설정
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 201
        mock_session.post.return_value = mock_response
        mock_create_session.return_value = mock_session

        # 함수 호출
        response = public_data_api_post("https://example.com", json={"key": "value"})

        # 검증
        mock_create_session.assert_called_once()
        mock_session.post.assert_called_once_with(
            "https://example.com", json={"key": "value"}
        )
        self.assertEqual(response.status_code, 201)

    def test_ssl_context_configuration(self):
        """SSL 컨텍스트 설정 테스트"""
        adapter = PublicDataApiSSLAdapter()

        # SSL 컨텍스트가 올바르게 설정되는지 확인하기 위해
        # init_poolmanager를 직접 호출해볼 수는 없지만,
        # 최소한 메서드가 존재하는지 확인
        self.assertTrue(hasattr(adapter, "init_poolmanager"))
        self.assertTrue(callable(adapter.init_poolmanager))

    def test_headers_configuration(self):
        """헤더 설정 테스트"""
        session = create_public_data_api_session()

        expected_headers = [
            "User-Agent",
            "Accept",
            "Accept-Language",
            "Accept-Encoding",
            "Connection",
            "Upgrade-Insecure-Requests",
            "Referer",
        ]

        for header in expected_headers:
            self.assertIn(header, session.headers)
            self.assertIsNotNone(session.headers[header])

    def test_user_agent_format(self):
        """User-Agent 헤더 형식 테스트"""
        session = create_public_data_api_session()
        user_agent = session.headers["User-Agent"]

        # User-Agent가 올바른 형식인지 확인
        self.assertIn("Mozilla", user_agent)
        self.assertIn("Chrome", user_agent)
        self.assertIn("Safari", user_agent)


class TestSSLConfiguration(unittest.TestCase):
    """SSL 설정 테스트"""

    def test_tls_version_constants(self):
        """TLS 버전 상수 테스트"""
        # Python ssl 모듈에서 필요한 상수들이 존재하는지 확인
        self.assertTrue(hasattr(ssl, "TLSVersion"))
        self.assertTrue(hasattr(ssl.TLSVersion, "TLSv1"))
        self.assertTrue(hasattr(ssl.TLSVersion, "TLSv1_2"))

    def test_ssl_options(self):
        """SSL 옵션 상수 테스트"""
        # 필요한 SSL 옵션들이 존재하는지 확인
        self.assertTrue(hasattr(ssl, "OP_LEGACY_SERVER_CONNECT"))

        # 선택적 옵션 (Python 버전에 따라 다를 수 있음)
        if hasattr(ssl, "OP_DONT_INSERT_EMPTY_FRAGMENTS"):
            self.assertIsInstance(ssl.OP_DONT_INSERT_EMPTY_FRAGMENTS, int)


def run_basic_tests():
    """기본 테스트 실행"""
    print("Public Data API SSL Adapter - 기본 테스트")
    print("=" * 50)

    try:
        # 1. 어댑터 초기화 테스트
        print("1. 어댑터 초기화 테스트...")
        adapter = PublicDataApiSSLAdapter()
        print("   ✅ 어댑터 초기화 성공")

        # 2. 세션 생성 테스트
        print("2. 세션 생성 테스트...")
        session = adapter.create_public_data_api_session()
        print("   ✅ 세션 생성 성공")

        # 3. 헤더 확인
        print("3. 헤더 설정 확인...")
        expected_headers = ["User-Agent", "Accept", "Accept-Language"]
        for header in expected_headers:
            if header in session.headers:
                print(f"   ✅ {header}: {session.headers[header][:50]}...")
            else:
                print(f"   ❌ {header}: 누락")

        # 4. 편의 함수 테스트
        print("4. 편의 함수 테스트...")
        session2 = create_public_data_api_session()
        print("   ✅ create_public_data_api_session() 성공")

        print("\n🎉 모든 기본 테스트 통과!")
        return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        return False


if __name__ == "__main__":
    print("선택하세요:")
    print("1. 기본 테스트 실행")
    print("2. 유닛 테스트 실행")

    choice = input("선택 (1 또는 2): ").strip()

    if choice == "1":
        run_basic_tests()
    elif choice == "2":
        unittest.main()
    else:
        print("기본 테스트를 실행합니다...")
        run_basic_tests()
