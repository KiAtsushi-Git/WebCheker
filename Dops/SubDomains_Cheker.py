import socket
import itertools
import argparse
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import tldextract


def generate_common_subdomains():
    common_subdomains = [
        'www', 'mail', 'blog', 'dev', 'test', 'shop', 'api', 'forum', 'help', 'portal', 'news',
        'images', 'cdn', 'web', 'home', 'dashboard', 'app', 'beta', 'staging', 'admin', 'assets',
        'auth', 'backup', 'billing', 'calendar', 'cdn', 'chat', 'client', 'cloud', 'community', 'config', 'connect',
        'console', 'content', 'db', 'data', 'database', 'demo', 'dns', 'docs', 'download', 'edge', 'email', 'events',
        'files', 'ftp', 'gateway', 'git', 'go', 'graphql', 'hub', 'img', 'internal', 'inventory', 'iot', 'js',
        'lab', 'login', 'logs', 'main', 'manage', 'marketing', 'media', 'monitor', 'mx', 'net', 'node', 'notes', 'ns',
        'partners', 'payment', 'photos', 'pop', 'prod', 'profile', 'project', 'proxy', 'public', 'redis', 'reports',
        'resources', 'rest', 'review', 'router', 'rss', 'sandbox', 'search', 'secure', 'server', 'service', 'services',
        'site', 'smtp', 'source', 'sql', 'sso', 'staff', 'stage', 'static', 'status', 'storage', 'support', 'sys',
        'task', 'team', 'terms', 'tools', 'tracking', 'trade', 'training', 'upload', 'user', 'v1', 'v2', 'v3',
        'video', 'vpn', 'webmail', 'wiki', 'work', 'www1', 'www2', 'www3', 'ww', 'dev1', 'dev2', 'app1', 'app2',
        'test1', 'test2', 'mail1', 'mail2', 'store', 'connect', 'secure', 'media', 'prod', 'analytics', 'events',
        'gateway', 'billing', 'pay', 'bank', 'partners', 'community', 'prod', 'stg', 'qa', 'docs', 'crm', 'erp',
        'support', 'beta', 'test', 'jobs', 'reports', 'labs', 'dashboard', 'account', 'service', 'devops', 'oauth', 'monitor',
        'admin', 'node', 'cdn1', 'cdn2', 'cdn3', 'ns1', 'ns2', 'ns3', 'dns1', 'dns2', 'dns3', 'edge1', 'edge2',
        'logistics', 'trace', 'status', 'api1', 'api2', 'api3', 'payments', 'billing', 'order', 'resources', 'download',
        'helpdesk', 'crm', 'company', 'investor', 'support', 'press', 'about', 'partners', 'shop', 'gallery',
        'cdnassets', 'usercontent', 'mediafiles', 'cloudfront', 'staticassets', 'delivery', 'feedback', 'locale', 'help',
        'sitemap', 'terms', 'privacy', 'legal', 'policies', 'reviews', 'upgrades', 'signin', 'register', 'signup',
        'downloads', 'videos', 'images', 'payment', 'rewards', 'dashboard', 'games', 'legal', 'api4', 'api5', 'content1',
        'content2', 'support1', 'support2', 'order1', 'order2', 'store1', 'store2', 'search1', 'search2', 'secure1',
        'secure2', 'static1', 'static2', 'files1', 'files2', 'ftp1', 'ftp2', 'blog1', 'blog2', 'docs1', 'docs2', 'cdn4', 'cdn5',
        'cdn6', 'cdn7', 'cdn8', 'public1', 'public2', 'public3', 'media1', 'media2', 'media3', 'uploads1', 'uploads2',
        'events1', 'events2', 'events3', 'chat1', 'chat2', 'chat3', 'monitor1', 'monitor2', 'monitor3', 'status1', 'status2',
        'status3', 'tracking1', 'tracking2', 'tracking3', 'feedback1', 'feedback2', 'feedback3', 'legal1', 'legal2', 'legal3',
        'admin1', 'admin2', 'admin3', 'tools1', 'tools2', 'tools3', 'payments1', 'payments2', 'payments3', 'payments4', 'payments5',
        'admin4', 'admin5', 'secure3', 'secure4', 'secure5', 'order3', 'order4', 'order5', 'store3', 'store4', 'store5',
        'cloudfront1', 'cloudfront2', 'cloudfront3', 'cloudfront4', 'cdn9', 'cdn10', 'cdn11', 'cdn12', 'cdn13', 'cdn14', 'cdn15',
        'cdn16', 'cdn17', 'cdn18', 'files3', 'files4', 'files5', 'files6', 'data1', 'data2', 'data3', 'data4', 'data5',
        'data6', 'data7', 'data8', 'data9', 'data10', 'profile1', 'profile2', 'profile3', 'profile4', 'profile5', 'prod1',
        'prod2', 'prod3', 'prod4', 'prod5', 'cdn19', 'cdn20', 'cdn21', 'cdn22', 'cdn23', 'cdn24', 'cdn25', 'cdn26', 'cdn27',
        'cdn28', 'cdn29', 'cdn30', 'secure6', 'secure7', 'secure8', 'secure9', 'secure10', 'docs3', 'docs4', 'docs5', 'docs6',
        'helpdesk1', 'helpdesk2', 'helpdesk3', 'helpdesk4', 'helpdesk5', 'test3', 'test4', 'test5', 'test6', 'dev3', 'dev4', 'dev5',
        'dev6', 'dev7', 'dev8', 'dev9', 'app3', 'app4', 'app5', 'app6', 'app7', 'app8', 'qa1', 'qa2', 'qa3', 'qa4', 'qa5',
        'monitor4', 'monitor5', 'monitor6', 'monitor7', 'monitor8', 'monitor9', 'account1', 'account2', 'account3',
        'account4', 'account5', 'logs1', 'logs2', 'logs3', 'logs4', 'logs5', 'logs6', 'logs7', 'logs8', 'logs9', 'logs10', 'logs11',
        'logs12', 'logs13', 'logs14', 'logs15', 'logs16', 'logs17', 'logs18', 'test7', 'test8', 'test9', 'test10',
        'web1', 'web2', 'web3', 'web4', 'web5', 'web6', 'web7', 'web8', 'web9', 'web10', 'web11', 'web12', 'web13', 'web14',
        'web15'
    ] + [f"{prefix}{i}" for prefix in ['app', 'dev', 'test', 'prod', 'api', 'stage', 'cdn'] for i in range(50)]

    return common_subdomains


def check_subdomain_dns(domain, subdomain):
    full_domain = f"{subdomain}.{domain}"
    try:
        ip_address = socket.gethostbyname(full_domain)
        return full_domain, ip_address
    except socket.gaierror:
        return full_domain, None


def find_subdomains(domain):
    subdomains_found_with_ip = {}
    subdomains_found_without_ip = []
    subdomains_to_check = generate_common_subdomains()

    with ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(check_subdomain_dns, domain, sub) for sub in subdomains_to_check]

        for future in futures:
            result = future.result()
            subdomain, ip = result
            if ip:
                subdomains_found_with_ip[subdomain] = ip
            else:
                subdomains_found_without_ip.append(subdomain)

    print(f"\n[{domain}] subdomains with IP:")
    for subdomain, ip in subdomains_found_with_ip.items():
        print(f"┣ [+] {subdomain} - {ip}")
    print("┗——————————————————————————————")


def extract_domain_from_url(url):
    parsed_url = urlparse(url)
    extracted = tldextract.extract(parsed_url.netloc)
    return f"{extracted.domain}.{extracted.suffix}"


def SubDom_Check(url=None):
    if url:
        domain = extract_domain_from_url(url)
    else:
        parser = argparse.ArgumentParser(description="Subdomain checker")
        parser.add_argument("-U", "--url", type=str, help="URL to extract the domain from and check subdomains")
        parser.add_argument("-URL", "--long-url", type=str, help="Full URL to extract the domain from and check subdomains")

        args = parser.parse_args()

        if args.url:
            domain = extract_domain_from_url(args.url)
        elif args.long_url:
            domain = extract_domain_from_url(args.long_url)
        else:
            domain = input("Enter the domain to check: ")

    find_subdomains(domain)

if __name__ == "__main__":
    SubDom_Check()