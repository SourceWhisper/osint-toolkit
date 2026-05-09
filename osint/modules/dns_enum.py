import dns.resolver

RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

def run(target, config):
    results = {}
    for rtype in RECORD_TYPES:
        try:
            answers = dns.resolver.resolve(target, rtype)
            results[rtype] = [str(r) for r in answers]
        except Exception:
            results[rtype] = []
    return results
