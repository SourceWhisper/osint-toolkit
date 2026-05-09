import requests
import dns.resolver
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(target, config):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["8.8.8.8", "1.1.1.1"]
        answer = resolver.resolve("crt.sh", "A")
        ip = str(answer[0])

        r = requests.get(
            f"https://{ip}/?q=%.{target}&output=json",
            timeout=90,
            headers={
                "Host": "crt.sh",
                "User-Agent": "osint-toolkit"
            },
            verify=False
        )

        if not r.text.strip():
            return {"subdomains": [], "count": 0, "note": "No CT logs found"}

        try:
            data = r.json()
        except Exception:
            return {"subdomains": [], "count": 0, "note": "crt.sh returned invalid response"}

        subdomains = set()
        for entry in data:
            for sub in entry.get("name_value", "").split("\n"):
                if sub.endswith(target):
                    subdomains.add(sub.strip())

        return {"subdomains": sorted(subdomains), "count": len(subdomains)}

    except Exception as e:
        return {"error": str(e)}
