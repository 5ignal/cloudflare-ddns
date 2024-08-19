import requests
import json

class cloudflare_ddns():
    def __init__(self, domain: str, token: str, proxy: bool, webhook: str):
        self.cloudflare_api = "https://api.cloudflare.com/client/v4/zones"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        ipAddr = self.getIP()
        splitDomain = domain.split(".")
        if len(splitDomain) == 2:
            splitDomain = domain
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
            self.discord(webhook, update, domain, ipAddr, self.getIdAccount(), splitDomain)

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
            return True
        else:
            print("DNS Update Failed")
            print(response.text)
            return False

    def getIdAccount(self):
        response = requests.get(
            "https://api.cloudflare.com/client/v4/accounts",
            headers=self.headers)
        data = json.loads(response.text)["result"]
        if data[0]:
            return data[0]['id']
        else:
            print("Account Not Found")

    def discord(self, webhook, update, domain, ipAddr, idAccount, idZone):
        color = int("e7883b", 16) if update else int("e01e5a", 16)
        text = "Success" if update else "Failed"

        author_url = f"https://dash.cloudflare.com/{idAccount}/{idZone}/dns/records"
        icon_url = "https://yt3.googleusercontent.com/lyrJ4UAHQLNGpkLQbL03Xh6GJvAZxA1loSDBRYPWuRbssAoEdCsN0DeybqdKNiJH7KA9NsoH-w=s900-c-k-c0x00ffffff-no-rj"

        payload = dict()
        payload["content"] = "@here"
        payload["embeds"] = list()
        payload_embed = dict()
        payload_embed["color"] = color
        payload_embed["author"] = dict([("name", "Cloudflare"), ("url", author_url), ("icon_url", icon_url)])
        payload_embed["fields"] = [dict([("name", "A Record"), ("value", domain), ("inline", True)]),
                               dict([("name", "IP Address"), ("value", ipAddr), ("inline", True)])]
        payload_embed["title"] = f"DDNS Update {text}"
        payload["embeds"].append(payload_embed)

        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook, data=json.dumps(payload), headers=headers)
        print(response.status_code, response.text)

if __name__ == "__main__":
    with open("./config.json", "r") as f:
        inp = json.load(f)
    for i in inp:
        cloudflare_ddns(i["cloudflare_domain"], i["cloudflare_api_token"], i["cloudflare_proxy"], i["webhook"])