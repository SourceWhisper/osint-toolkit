import requests

def run(target, config):
    api_key = config.get("hibp_api_key", "")
    if not api_key:
        return {"skipped": "No HIBP API key"}
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "osint-toolkit"
    }
    r = requests.get(
        f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}",
        headers=headers,
        timeout=10
    )
    if r.status_code == 404:
        return {"breached": False, "breaches": []}
    elif r.status_code == 200:
        breaches = r.json()
        return {
            "breached": True,
            "count": len(breaches),
            "breaches": [
                {
                    "name": b["Name"],
                    "date": b["BreachDate"],
                    "data_classes": b["DataClasses"]
                }
                for b in breaches
            ]
        }
    return {"error": f"HTTP {r.status_code}"}
