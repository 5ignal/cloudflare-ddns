import requests
import json

class cloudflare_ddns():
    def __init__(self, token, domain, sub_domain):
        self.domain = domain
        self.sub_domain = sub_domain
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

        wantName = "%s.%s"%(self.sub_domain, self.domain)
        for record in data['result']:
            if[record['type'] == 'A' and record['name'] == wantName]:
                return ''.join(record['id'])
        print("Can't find Domain")
        return -1


    def record_update(self):
        payload = {
            'type': 'A',
            'content': self.get_ip()
        }
        if self.sub_domain == "":
            payload['name'] = self.domain
        else:
            payload['name'] = self.sub_domain
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
    # Domain
    cloudflare_domain = "DOMAIN"

    # Sub Domain
    # If you want to apply it to A record, leave it blank
    cloudflare_sub_domain = "SUB_DOMAIN"

    # Cloudflare API token
    # https://dash.cloudflare.com/profile/api-tokens
    cloudflare_api_token = "API_TOKEN"

    cloudflare_ddns(cloudflare_api_token, cloudflare_domain, cloudflare_sub_domain)