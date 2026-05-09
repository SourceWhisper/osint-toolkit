import requests
import dns.resolver
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(target, config):
    if target.endswith(".br"):
        return _run_registro_br(target)
    return _run_rdap(target)


def _run_registro_br(target):
    try:
        res = dns.resolver.Resolver()
        res.nameservers = ["8.8.8.8", "1.1.1.1"]
        ip = str(res.resolve("rdap.registro.br", "A")[0])

        response = requests.get(
            f"https://{ip}/domain/{target}",
            headers={"Host": "rdap.registro.br"},
            timeout=15,
            verify=False
        )
        response.raise_for_status()
        data = response.json()

        registrar = None
        emails = []
        for entity in data.get("entities", []):
            vcard = entity.get("vcardArray", [[], []])[1]
            name  = next((v[3] for v in vcard if v[0] == "fn"), None)
            email = next((v[3] for v in vcard if v[0] == "email"), None)
            if email:
                emails.append({"role": entity.get("roles"), "name": name, "email": email})
            if "registrar" in entity.get("roles", []):
                registrar = name

        nameservers = [ns["ldhName"] for ns in data.get("nameservers", [])]
        events      = {e["eventAction"]: e["eventDate"] for e in data.get("events", [])}

        return {
            "provider":        "registro.br",
            "registrar":       registrar,
            "creation_date":   events.get("registration"),
            "expiration_date": events.get("expiration"),
            "last_changed":    events.get("last changed"),
            "name_servers":    nameservers,
            "status":          data.get("status", []),
            "contacts":        emails,
        }

    except Exception as e:
        return {"error": str(e)}


def _run_rdap(target):
    try:
        res = dns.resolver.Resolver()
        res.nameservers = ["8.8.8.8", "1.1.1.1"]
        ip = str(res.resolve("rdap.org", "A")[0])

        r = requests.get(
            f"https://{ip}/domain/{target}",
            headers={"Host": "rdap.org"},
            timeout=20,
            verify=False
        )
        r.raise_for_status()
        data = r.json()

        registrar = None
        for entity in data.get("entities", []):
            if "registrar" in entity.get("roles", []):
                vcard     = entity.get("vcardArray", [[], []])[1]
                registrar = next((v[3] for v in vcard if v[0] == "fn"), None)

        nameservers = [ns["ldhName"] for ns in data.get("nameservers", [])]
        events      = {e["eventAction"]: e["eventDate"] for e in data.get("events", [])}

        return {
            "provider":        "rdap.org",
            "registrar":       registrar,
            "creation_date":   events.get("registration"),
            "expiration_date": events.get("expiration"),
            "last_changed":    events.get("last changed"),
            "name_servers":    nameservers,
            "status":          data.get("status", []),
        }

    except Exception as e:
        return {"error": str(e)}
