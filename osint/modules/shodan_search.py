import requests
import socket

def _resolve(hostname):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["8.8.8.8", "1.1.1.1"]
    answer = resolver.resolve(hostname, "A")
    return str(answer[0])

def run(target, config):
    api_key = config.get("shodan_api_key", "")

    # Tenta Shodan se tiver chave com créditos
    if api_key and api_key not in ("REVOGADA", "SUA_CHAVE_AQUI"):
        result = _run_shodan(target, api_key)
        if "skipped" not in result:
            return result

    # Fallback gratuito
    return _run_free(target)


def _run_shodan(target, api_key):
    try:
        import shodan
        api = shodan.Shodan(api_key)
        info = api.info()
        if info.get("query_credits", 0) == 0:
            return {"skipped": "no credits"}

        ip = socket.gethostbyname(target)
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
        ip = socket.gethostbyname(target)
        result = {"provider": "IPInfo + HackerTarget (free)"}

        # IPInfo — org, geo, hostname
        r = requests.get(
            f"https://ipinfo.io/{ip}/json",
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            result["ip"]       = data.get("ip")
            result["org"]      = data.get("org")
            result["country"]  = data.get("country")
            result["city"]     = data.get("city")
            result["hostname"] = data.get("hostname")

        # HackerTarget — port scan
        r2 = requests.get(
            f"https://api.hackertarget.com/nmap/?q={ip}",
            timeout=20
        )
        if r2.status_code == 200 and "error" not in r2.text.lower():
            result["port_scan"] = r2.text.strip()

        return result

    except Exception as e:
        return {"error": str(e)}
