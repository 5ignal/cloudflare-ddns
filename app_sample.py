import requests
import json

class cloudflare:
    def __init__(self, api_token, domain, record_name, proxy):
        self.api_endpoint = "https://api.cloudflare.com/client/v4/zones"
        self.domain = domain
        if record_name == "":
            self.record = domain
        else:
            self.record = f"{record_name}.{domain}"
        self.proxy = proxy
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    # 현재 IP 주소 가져오기
    def get_current_ip(self):
        return requests.get("https://myip.wtf/text").text

    # 도메인 이름을 이용하여 Zone ID 가져오기
    def get_zone_id(self):
        params = {
            "name": self.domain
        }
        response = requests.get(self.api_endpoint, headers=self.headers, params=params)
        data = json.loads(response.text)["result"]
        if len(data) > 0:
            return data[0]["id"]
        print("Zone ID를 찾을 수 없습니다.")

    # DNS 레코드 조회하기
    def get_dns_record(self):
        params = {
            "type": "A",
            "name": self.record
        }
        response = requests.get(f"{self.api_endpoint}/{self.zone_id}/dns_records", headers=self.headers, params=params)
        data = json.loads(response.text)["result"]
        if len(data) > 0:
            return data[0]
        print("DNS 레코드를 찾을 수 없습니다.")

    # DNS 레코드 업데이트하기
    def update_dns_record(self):
        self.ip = self.get_current_ip()
        self.zone_id = self.get_zone_id()
        if self.zone_id is not None:
            record = self.get_dns_record()
            if record is not None:
                data = {
                    "type": "A",
                    "name": self.record,
                    "content": self.ip
                }
                if self.proxy:
                    data["proxied"] = True
                response = requests.put(f"{self.api_endpoint}/{self.zone_id}/dns_records/{record['id']}", headers=self.headers, data=json.dumps(data))
                result = json.loads(response.text)
                if result.get('success') == True:
                    print("DNS 레코드가 업데이트되었습니다.")
                    return 0
        print("DNS 레코드 업데이트에 실패했습니다.")

if __name__ == "__main__":
    # Cloudflare API 토큰 
    # https://dash.cloudflare.com/profile/api-tokens
    # Zone:DNS:Edit
    # Global API Key 사용할 수 없음
    API_TOKEN = ""

    # 도메인 이름
    DOMAIN = "example.com"

    # 서브 도메인 이름 (없으면 빈 문자열)
    RECORD_NAME = ""

    # Cloudflare Proxy 사용 여부
    PROXY = True

    # Cloudflare 객체 생성
    cf = cloudflare(API_TOKEN, DOMAIN, RECORD_NAME, PROXY)
    cf.update_dns_record()
