import requests
import json

class cloudflare_ddns():
    def __init__(self, domain: str, token: str, proxy: bool):
        self.cloudflare_api = 'https://api.cloudflare.com/client/v4/zones'
        self.headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        }

        ipAddr = self.getIP()
        splitDomain = domain.split('.')
        if len(splitDomain) == 2:
            idZone = self.getIdZone(domain)
        else:
            idZone = self.getIdZone(f'{splitDomain[1]}.{splitDomain[2]}')
        idRecord = self.getIdRecord(idZone, domain)
        self.update(domain, idZone, idRecord, ipAddr, proxy)

    def getIP(self) -> str:
        res = requests.get("https://myip.ogunaru.workers.dev").text
        res = res.replace('\n', '')
        return res

    def getIdZone(self, domain):
        response = requests.get(
            f'{self.cloudflare_api}?name={domain}',
            headers=self.headers,
        )
        data = json.loads(response.text)
        return data["result"][0]["id"]

    def getIdRecord(self, idZone, domain):
        response = requests.get(
            f'{self.cloudflare_api}/{idZone}/dns_records?name={domain}',
            headers=self.headers,
        )
        data = json.loads(response.text)
        if data['result']:
            return data['result'][0]['id']
        else:
            return None

    def update(self, domain, idZone, idRecord, ipAddr, proxy):
        payload = {
            'type': 'A',
            'content': ipAddr
        }
        payload['name'] = domain
        if proxy:
            payload["proxied"] = True
        response = requests.put(
            f'{self.cloudflare_api}/{idZone}/dns_records/{idRecord}',
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
    with open('./cloudflareUpdaterInp.json', 'r') as f:
        inp = json.load(f)
    cloudflare_ddns(inp["cloudflare_domain"], inp["cloudflare_api_token"], inp["cloudflare_proxy"])
