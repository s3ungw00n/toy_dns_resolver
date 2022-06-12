import pytest
import requests
import resolver
import dns.ipv4

def test_resolve():
    ip = resolver.resolve('naver.com', '198.41.0.4')
    try:
        dns.ipv4.inet_aton(ip)
    except Exception:
        pytest.fail(f'not valid ip {ip}')

    response = requests.get(f'http://{ip}')
    assert(response.status_code == 200)
    assert('naver' in response.text)
