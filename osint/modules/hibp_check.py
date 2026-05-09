import requests

def run(target, config):
    hibp_key   = config.get("hibp_api_key", "")
    hunter_key = config.get("hunter_api_key", "")

    # Prioriza HIBP se tiver chave válida
    if hibp_key and hibp_key != "sua_key_aqui":
        return _run_hibp(target, hibp_key)

    # Fallback pro Hunter.io
    if hunter_key:
        return _run_hunter(target, hunter_key)

    return {"skipped": "No email intel API configured — add hibp_api_key or hunter_api_key to config.yaml"}


def _run_hibp(target, api_key):
    try:
        r = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}",
            headers={
                "hibp-api-key": api_key,
                "user-agent":   "osint-toolkit"
            },
            timeout=10
        )
        if r.status_code == 404:
            return {"provider": "HaveIBeenPwned", "breached": False, "breaches": []}
        elif r.status_code == 200:
            breaches = r.json()
            return {
                "provider": "HaveIBeenPwned",
                "breached": True,
                "count":    len(breaches),
                "breaches": [
                    {
                        "name":         b["Name"],
                        "date":         b["BreachDate"],
                        "data_classes": b["DataClasses"]
                    }
                    for b in breaches
                ]
            }
        return {"provider": "HaveIBeenPwned", "error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"provider": "HaveIBeenPwned", "error": str(e)}


def _run_hunter(target, api_key):
    try:
        r = requests.get(
            f"https://api.hunter.io/v2/email-verifier?email={target}&api_key={api_key}",
            timeout=10
        )
        data = r.json().get("data", {})
        return {
            "provider":   "Hunter.io",
            "status":     data.get("status"),
            "score":      data.get("score"),
            "disposable": data.get("disposable"),
            "mx_records": data.get("mx_records"),
            "smtp_server":data.get("smtp_server"),
            "smtp_check": data.get("smtp_check"),
        }
    except Exception as e:
        return {"provider": "Hunter.io", "error": str(e)}
