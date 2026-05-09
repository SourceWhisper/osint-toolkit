import importlib
import yaml
from osint.reporter import generate_report

MODULES_MAP = {
    "ip":     ["ip_geo", "shodan_search"],
    "domain": ["whois_lookup", "dns_enum", "subdomain_finder", "shodan_search"],
    "email": ["hibp_check"],
}

def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)

def run_investigation(target, target_type, output_fmt, selected_modules=None):
    config = load_config()
    modules_to_run = selected_modules or MODULES_MAP.get(target_type, [])
    results = {"target": target, "type": target_type, "modules": {}}

    for mod_name in modules_to_run:
        try:
            mod = importlib.import_module(f"osint.modules.{mod_name}")
            print(f"[*] Running {mod_name}...")
            results["modules"][mod_name] = mod.run(target, config)
        except Exception as e:
            results["modules"][mod_name] = {"error": str(e)}

    generate_report(results, output_fmt)
