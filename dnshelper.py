import whois
def make_whois_query(domain):
    # get the domain details
    domain_details = whois.whois(domain)
    return domain_details