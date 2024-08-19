import requests
import json

class cloudflare_ddns():
    def __init__(self, domain: str, token: str, proxy: bool):
        self.cloudflare_api = "https://api.cloudflare.com/client/v4/zones"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        ipAddr = self.getIP()
        splitDomain = domain.split(".")
        if len(splitDomain) == 2:
            idZone = self.getIdZone(domain)
        else:
            splitDomain = f"{splitDomain[1]}.{splitDomain[2]}"
            idZone = self.getIdZone(splitDomain)
        record = self.getRecord(idZone, domain)
        if record[1] == ipAddr:
            print("No Update Needed")
            return
        else:
            update = self.update(domain, idZone, record[0], ipAddr, proxy)

    def getIP(self) -> str:
        res = requests.get("https://myip.ogunaru.workers.dev").text
        return res

    def getIdZone(self, domain):
        response = requests.get(
            f"{self.cloudflare_api}?name={domain}",
            headers=self.headers,
        )
        data = json.loads(response.text)
        if data["success"]:
            return data["result"][0]["id"]
        else:
            print("Zone Not Found")

    def getRecord(self, idZone, domain):
        response = requests.get(
            f"{self.cloudflare_api}/{idZone}/dns_records?name={domain}",
            headers=self.headers,
        )
        data = json.loads(response.text)
        if data["success"]:
            IdRecord = data["result"][0]["id"]
            ValueRecord = data["result"][0]["content"]
            return IdRecord, ValueRecord
        else:
            print("DNS Record Not Found")

    def update(self, domain, idZone, idRecord, ipAddr, proxy):
        payload = {"type": "A", "content": ipAddr, "name": domain}
        if proxy:
            payload["proxied"] = True
        response = requests.put(
            f"{self.cloudflare_api}/{idZone}/dns_records/{idRecord}",
            headers=self.headers,
            json=payload,
        )
        data = json.loads(response.text)
        if data.get("success") == True:
            print("DNS Update Success")
        else:
            print("DNS Update Failed")
            print(response.text)

if __name__ == "__main__":
    with open("./config.json", "r") as f:
        inp = json.load(f)
    for i in inp:
        cloudflare_ddns(i["cloudflare_domain"], i["cloudflare_api_token"], i["cloudflare_proxy"])
