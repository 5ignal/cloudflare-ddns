# cloudflare-ddns

Cloudflare DDNS를 지원하지 않는 환경에서 사용하기 위해 만들어졌습니다.

```py
    # Cloudflare API 토큰 
    # https://dash.cloudflare.com/profile/api-tokens
    # Zone:DNS:Edit
    # Global API Key 사용할 수 없음
    API_TOKEN = ""

    # 도메인 이름
    DOMAIN = "example.com"

    # 서브 도메인 이름 (없으면 빈 문자열)
    RECORD_NAME = ""
```
