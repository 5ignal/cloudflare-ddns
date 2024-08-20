import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

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
            update_result = 0
        else:
            update_result = self.update(domain, idZone, record[0], ipAddr, proxy)
        if webhook:
            self.discord(webhook, update_result, domain, ipAddr, self.getIdAccount(), splitDomain)

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
            return 1
        else:
            print("DNS Update Failed")
            print(response.text)
            return -1

    def getIdAccount(self):
        response = requests.get(
            "https://api.cloudflare.com/client/v4/accounts",
            headers=self.headers)
        data = json.loads(response.text)["result"]
        if data[0]:
            return data[0]['id']
        else:
            print("Account Not Found")

    def discord(self, webhook_url, update_result, domain, ipAddr, idAccount, idZone):
        author_url = f"https://dash.cloudflare.com/{idAccount}/{idZone}/dns/records"
        icon_url = "https://yt3.googleusercontent.com/lyrJ4UAHQLNGpkLQbL03Xh6GJvAZxA1loSDBRYPWuRbssAoEdCsN0DeybqdKNiJH7KA9NsoH-w=s900-c-k-c0x00ffffff-no-rj"

        if update_result == 0:
            title="No Update Needed"
            description=f"DNS Record for {domain} is already updated to {ipAddr}"
            color=int("5865f2", 16)
            content = ""
        elif update_result == 1:
            title = "DNS Update Success"
            description = f"DNS Record for {domain} has been updated to {ipAddr}"
            color = int("e7883b", 16)
            content = "@here"
        else:
            title="DNS Update Failed" 
            description=f"DNS Record for {domain} failed to update to {ipAddr}"
            color=int("e01e5a", 16)
            content = "@here"

        webhook = DiscordWebhook(url=webhook_url, content=content)

        embed = DiscordEmbed(title=title, description=description, color=color)
        embed.set_author(name="Cloudflare", url=author_url, icon_url=icon_url)
        embed.add_embed_field(name="A Record", value=domain, inline=True)
        embed.add_embed_field(name="IP Address", value=ipAddr, inline=True)
        embed.set_timestamp()

        webhook.add_embed(embed)
        webhook.execute()

if __name__ == "__main__":
    with open("./config.json", "r") as f:
        inp = json.load(f)
    for i in inp:
        cloudflare_ddns(i["cloudflare_domain"], i["cloudflare_api_token"], i["cloudflare_proxy"], i.get("webhook", None))