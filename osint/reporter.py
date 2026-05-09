import json
from datetime import datetime

def generate_report(results, fmt):
    if fmt == "terminal":
        print(json.dumps(results, indent=2, default=str))
    elif fmt == "json":
        fname = f"report_{results['target']}_{datetime.now():%Y%m%d_%H%M}.json"
        with open(fname, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"[+] Report saved: {fname}")
    elif fmt == "html":
        _generate_html(results)

def _generate_html(results):
    fname = f"report_{results['target']}_{datetime.now():%Y%m%d_%H%M}.html"
    # Aqui você usa Jinja2 para renderizar um template HTML limpo
    # com tabelas por módulo, badges coloridos para vulns, etc.
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("templates/"))
    tmpl = env.get_template("report.html")
    html = tmpl.render(data=results, generated_at=datetime.now())
    with open(fname, "w") as f:
        f.write(html)
    print(f"[+] HTML report: {fname}")
