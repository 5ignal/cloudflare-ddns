# cloudflare-ddns

Cloudflare DDNS를 지원하지 않는 환경에서 사용하기 위해 만들어졌습니다.

[![windows-build-release](https://github.com/5ignal/cloudflare-ddns/actions/workflows/windows-build-release.yml/badge.svg)](https://github.com/5ignal/cloudflare-ddns/actions/workflows/windows-build-release.yml)
[![docker-build-push](https://github.com/5ignal/cloudflare-ddns/actions/workflows/docker-build-push.yml/badge.svg)](https://github.com/5ignal/cloudflare-ddns/actions/workflows/docker-build-push.yml)

### config.json
```json
[
    {
        "cloudflare_domain": "example.com",
        "cloudflare_api_token": "ABCEFGHIJKLMNOPQRSTUVWXYZ",
        "cloudflare_proxy": true
    },
    {
        "cloudflare_domain": "example2.com",
        "cloudflare_api_token": "ABCEFGHIJKLMNOPQRSTUVWXYZ",
        "cloudflare_proxy": true,
        "webhook": "YOUR_DISCORD_WEBHOOK_URL"
    }
]

```
