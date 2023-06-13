import requests
import json

class cloudflare_ddns():
    def __init__(self, domain, token):
        self.domain = domain
        self.token = token
        self.headers = {
        'Authorization': f'Bearer {self.token}',
        'Content-Type': 'application/json',
        }
        self.cloudflare_api = 'https://api.cloudflare.com/client/v4/zones'
        self.get_zone_id()
        self.record_update()


    def get_ip(self):
        response = requests.get("https://myip.wtf/text")
        return response.text


    def get_zone_id(self):
        response = requests.get(
            f'{self.cloudflare_api}?name={self.domain}',
            headers=self.headers,
        )
        data = json.loads(response.text)
        self.zone_id = data["result"][0]["id"]


    def get_record_id(self):
        response = requests.get(
            f'{self.cloudflare_api}/{self.zone_id}/dns_records',
            headers=self.headers,
        )
        data = json.loads(response.text)
        a_record = [record['id'] for record in data["result"] if record["type"] == "A"]
        return ''.join(a_record)


    def record_update(self):
        payload = {
            'type': 'A',
            'name': self.domain,
            'content': self.get_ip()
        }
        response = requests.put(
            f'{self.cloudflare_api}/{self.zone_id}/dns_records/{self.get_record_id()}',
            headers=self.headers,
            json=payload,
        )
        data = json.loads(response.text)
        if data.get('success') == True:
            print('DNS Update Success')
        else:
            print('DNS Update Failed')
            print(response.text)


if __name__ == "__main__":
    # Cloudflare Domain
    cloudflare_domain = "YOUR.DOMAIN"

    # Cloudflare API token
    # https://dash.cloudflare.com/profile/api-tokens
    cloudflare_api_token = "API_TOKEN"

    cloudflare_ddns(cloudflare_domain, cloudflare_api_token)