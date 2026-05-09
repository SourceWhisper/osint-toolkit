<div align="center">

```
 ██████╗ ███████╗██╗███╗   ██╗████████╗    ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
██║   ██║███████╗██║██╔██╗ ██║   ██║          ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║   
██║   ██║╚════██║██║██║╚██╗██║   ██║          ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║   
╚██████╔╝███████║██║██║ ╚████║   ██║          ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║   
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝  
```

**Passive OSINT reconnaissance framework for domains, IPs and emails**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-00ff41?style=flat-square)](LICENSE)
[![OSINT](https://img.shields.io/badge/Type-OSINT-ff6b35?style=flat-square)]()
[![Status](https://img.shields.io/badge/Status-Active-00ff41?style=flat-square)]()

by **[SourceWhisper](https://github.com/SourceWhisper)** · Mauricio S V Costa

</div>

---

> 🇧🇷 [Leia em Português](#português) · 🇺🇸 [Read in English](#english)

---

## Demo

[![asciicast](https://asciinema.org/a/qSCnoXCh9uxgJEwh.svg)](https://asciinema.org/a/qSCnoXCh9uxgJEwh)

## Screenshots

### Terminal Output
![Terminal](assets/terminal.png)

### HTML Report
![Report](assets/report.png)

## English

### What is this?

OSINT Toolkit is a modular CLI framework that aggregates public intelligence about a target — domain, IP, or email — from multiple sources and generates a unified report in HTML or JSON.

Built from scratch in Python. No GUI, no bloat — just clean terminal output and structured reports.

### Features

- [x] WHOIS / RDAP lookup with automatic **registro.br** support for `.br` domains
- [x] Full DNS enumeration (A, AAAA, MX, NS, TXT, CNAME, SOA)
- [x] Subdomain discovery via **Certificate Transparency logs** (crt.sh)
- [x] Host intel via **Shodan** (paid) with automatic fallback to **IPInfo + HackerTarget** (free)
- [x] Email verification via **HaveIBeenPwned** (paid) with automatic fallback to **Hunter.io** (free)
- [x] HTML report with hacker-themed dark UI
- [x] JSON report for pipeline integration
- [x] Modular architecture — add new modules without touching core logic
- [ ] IP geolocation map (roadmap)
- [ ] TheHarvester integration (roadmap)
- [ ] Async execution for faster scans (roadmap)

### Architecture

```
osint-toolkit/
├── main.py                  # CLI entry point (argparse)
├── config.yaml              # API keys (never commit this)
├── config.yaml.example      # Safe template to commit
├── requirements.txt
├── templates/
│   └── report.html          # Jinja2 HTML template
└── osint/
    ├── core.py              # Module orchestrator (dynamic import)
    ├── reporter.py          # HTML / JSON output
    └── modules/
        ├── whois_lookup.py  # RDAP + registro.br auto-detect
        ├── dns_enum.py      # dnspython full record scan
        ├── subdomain_finder.py  # crt.sh Certificate Transparency
        ├── shodan_search.py     # Shodan paid / IPInfo+HackerTarget free
        ├── hibp_check.py        # HIBP paid / Hunter.io free
        └── ip_geo.py            # (roadmap)
```

**Design decisions worth noting:**
- Uses `importlib` for dynamic module loading — new modules require zero changes to core
- Uses RDAP over HTTPS instead of legacy WHOIS port 43 — more reliable and firewall-friendly
- Forces DNS resolution via `8.8.8.8` / `1.1.1.1` inside Python for modules that need it, without touching system DNS
- Auto-detects paid vs free API tier and falls back gracefully — tool works out of the box with zero API keys

### Installation

```bash
git clone https://github.com/SourceWhisper/osint-toolkit
cd osint-toolkit

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt

# Configure API keys
cp config.yaml.example config.yaml
nano config.yaml
```

### API Keys

| Key | Provider | Cost | Used for |
|-----|----------|------|----------|
| `shodan_api_key` | [shodan.io](https://account.shodan.io) | Free (limited) / Paid | Host intel, open ports, CVEs |
| `hibp_api_key` | [haveibeenpwned.com](https://haveibeenpwned.com/API/Key) | ~$3.50/mo | Email breach check |
| `hunter_api_key` | [hunter.io](https://hunter.io) | Free (25/mo) | Email verification (fallback) |

> The tool works without any API keys. Shodan and HIBP modules degrade gracefully to free alternatives.

### Usage

```bash
# Investigate a domain
python3 main.py tesla.com --type domain --output html

# Investigate a .br government domain
python3 main.py campinas.sp.gov.br --type domain --output json

# Check an email
python3 main.py user@example.com --type email --output json

# Run specific modules only
python3 main.py github.com --type domain --modules whois_lookup dns_enum

# Print to terminal
python3 main.py example.com --type domain --output terminal
```

### Sample Output

Running against `campinas.sp.gov.br` (city government of Campinas, SP — Brazil):

```json
{
  "whois_lookup": {
    "provider": "registro.br",
    "creation_date": "1995-07-06T12:00:00Z",
    "name_servers": ["dns1e.sp.gov.br", "dns2e.sp.gov.br", "..."],
    "contacts": [{"role": ["technical"], "name": "Gerencia Internet PRODESP", "email": "csirt@sp.gov.br"}]
  },
  "subdomain_finder": {
    "count": 49,
    "subdomains": ["funcional.api-dev.gmc.campinas.sp.gov.br", "teste-desif.campinas.sp.gov.br", "..."] API de desenvolvimento exposta via CT logs, ambiente de teste do sistema fiscal
  },
  "shodan_search": {
    "provider": "IPInfo + HackerTarget (free)",
    "org": "AS53116 Inform\u00e1tica de Munic\u00edpios Associados S/A - IMA",
    "city": "Campinas",
    "country": "BR"
  }
}
```

> **Interesting finding:** The B******* city government website is hosted in Provo, Utah, USA (Unified Layer shared hosting). The SOA record reveals the internal sysadmin contact: `informatica.ian@********.sp.gov.br`. Certificate Transparency logs exposed `cpanel.**********.sp.gov.br` and `whm.dedi-14424353.**********.sp.gov.br` — control panels accessible from the public internet.

### Disclaimer

This tool is intended for **authorized security testing and educational purposes only**. Only use it against targets you own or have explicit written permission to test. The author is not responsible for any misuse or damage caused by this tool.

---

## Português

### O que é isso?

OSINT Toolkit é um framework CLI modular que agrega inteligência pública sobre um alvo — domínio, IP ou e-mail — de múltiplas fontes e gera um relatório unificado em HTML ou JSON.

Construído do zero em Python. Sem interface gráfica, sem dependências desnecessárias — apenas saída limpa no terminal e relatórios estruturados.

### Funcionalidades

- [x] WHOIS / RDAP com suporte automático ao **registro.br** para domínios `.br`
- [x] Enumeração DNS completa (A, AAAA, MX, NS, TXT, CNAME, SOA)
- [x] Descoberta de subdomínios via **Certificate Transparency logs** (crt.sh)
- [x] Inteligência de host via **Shodan** (pago) com fallback automático para **IPInfo + HackerTarget** (gratuito)
- [x] Verificação de e-mail via **HaveIBeenPwned** (pago) com fallback para **Hunter.io** (gratuito)
- [x] Relatório HTML com tema hacker dark
- [x] Relatório JSON para integração com pipelines
- [x] Arquitetura modular — adicione módulos sem modificar o núcleo
- [ ] Mapa de geolocalização de IP (roadmap)
- [ ] Integração com TheHarvester (roadmap)
- [ ] Execução assíncrona para scans mais rápidos (roadmap)

### Instalação

```bash
git clone https://github.com/SourceWhisper/osint-toolkit
cd osint-toolkit

# Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Configurar chaves de API
cp config.yaml.example config.yaml
nano config.yaml
```

### Uso

```bash
# Investigar um domínio
python3 main.py tesla.com --type domain --output html

# Investigar um domínio .gov.br
python3 main.py campinas.sp.gov.br --type domain --output json

# Verificar um e-mail
python3 main.py usuario@exemplo.com --type email --output json

# Rodar módulos específicos
python3 main.py github.com --type domain --modules whois_lookup dns_enum
```

### Decisões de Design

- `importlib` para carregamento dinâmico de módulos — novos módulos não exigem alteração no núcleo
- RDAP sobre HTTPS em vez da porta 43 legada do WHOIS — mais confiável e sem problemas de firewall
- Resolução DNS forçada via `8.8.8.8` / `1.1.1.1` dentro do Python para módulos que precisam, sem alterar o DNS do sistema
- Auto-detecção de tier pago vs gratuito com fallback gracioso — funciona sem nenhuma chave de API

### Aviso Legal

Esta ferramenta destina-se **exclusivamente a testes de segurança autorizados e fins educacionais**. Utilize apenas em alvos que você possui ou tem permissão explícita por escrito para testar. O autor não se responsabiliza por qualquer uso indevido.

---

<div align="center">

Made with 🖤 by [SourceWhisper](https://github.com/SourceWhisper)

*"The quieter you become, the more you are able to hear."*

</div>
