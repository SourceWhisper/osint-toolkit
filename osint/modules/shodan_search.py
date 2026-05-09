import requests
import socket
import dns.resolver
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def _resolve(hostname):
    res = dns.resolver.Resolver()
    res.nameservers = ["8.8.8.8", "1.1.1.1"]
    return str(res.resolve(hostname, "A")[0])

def run(target, config):
    api_key = config.get("shodan_api_key", "")
    if api_key and api_key not in ("REVOGADA", "SUA_CHAVE_AQUI"):
        result = _run_shodan(target, api_key)
        if "skipped" not in result:
            return result
    return _run_free(target)

def _run_shodan(target, api_key):
    try:
        import shodan
        api = shodan.Shodan(api_key)
        info = api.info()
        if info.get("query_credits", 0) == 0:
            return {"skipped": "no credits"}
        ip = _resolve(target)
        host = api.host(ip)
        return {
            "provider":     "Shodan",
            "organization": host.get("org"),
            "os":           host.get("os"),
            "ports":        host.get("ports"),
            "vulns":        list(host.get("vulns", [])),
            "hostnames":    host.get("hostnames"),
            "country":      host.get("country_name"),
            "last_update":  host.get("last_update"),
        }
    except Exception as e:
        return {"skipped": str(e)}

def _run_free(target):
    try:
        ip = _resolve(target)
        result = {"provider": "IPInfo + HackerTarget (free)"}

        ipinfo_ip = _resolve("ipinfo.io")
        r = requests.get(
            f"https://{ipinfo_ip}/{ip}/json",
            headers={"Host": "ipinfo.io"},
            timeout=10,
	    verify=False
        )
        if r.status_code == 200:
            data = r.json()
            result["ip"]       = data.get("ip")
            result["org"]      = data.get("org")
            result["country"]  = data.get("country")
            result["city"]     = data.get("city")
            result["hostname"] = data.get("hostname")

        return result

    except Exception as e:
        return {"error": str(e)}
