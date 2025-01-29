"""Dns records finder"""

import argparse
from urllib.parse import urlparse
import dns.resolver
import dns.exception

DNS_SERVER_NAMES = {
    "8.8.8.8": "Google DNS",
    "1.1.1.1": "Cloudflare DNS",
    "77.88.8.8": "Yandex DNS",
    "9.9.9.9": "Quad9 DNS",
    "208.67.222.222": "OpenDNS",
}

DEFAULT_DNS_SERVERS = ["8.8.8.8", "1.1.1.1", "77.88.8.8", "9.9.9.9", "208.67.222.222"]


def extract_domain(url):
    """Получение URL из запроса"""
    parsed_url = urlparse(url)
    return parsed_url.netloc or parsed_url.path


def get_dns_records(domain, dns_server):
    """Поиск днс записей"""
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]

    record_types = [
        "A",
        "AAAA",
        "MX",
        "TXT",
        "CNAME",
        "NS",
        "PTR",
        "SOA",
        "SRV",
        "CAA",
        "DS",
        "DNSKEY",
        "NSEC",
        "NSEC3",
        "TLSA",
        "SMIMEA",
        "LOC",
        "NAPTR",
        "HINFO",
        "MINFO",
        "RP",
    ]

    records = {}

    for record_type in record_types:
        try:
            answers = resolver.resolve(domain, record_type)
            records[record_type] = [str(answer) for answer in answers]
        except dns.resolver.NoAnswer:
            records[record_type] = f"Domain does " f"not support {record_type} records."
        except dns.resolver.NXDOMAIN:
            print(f"Domain {domain} does not exist.")
            break
        except dns.exception.DNSException as e:
            records[record_type] = f"Error: {e}"

    return records


def print_dns_records(records, dns_server):
    """Вывод пользователю днс записи"""
    dns_name = DNS_SERVER_NAMES.get(dns_server, "Unknown DNS")
    print(f"\nDNS [{dns_name}]: {dns_server}")

    found_any_record = False

    for record_type, values in records.items():
        if isinstance(values, list) and values:
            found_any_record = True
            print(f"[{record_type}] records:")
            for value in values:
                print(f" ┣ [+] {value}")
            print(" ┗——————————————————————————————")
        elif isinstance(values, str) and ("Domain does " "not support") not in values:
            found_any_record = True
            print(f" ┗ [-] {values}")

    if found_any_record:
        print()
    else:
        print(f"No DNS records found for {dns_server}\n")


def dns_rec(domain=None, dns_ip=None):
    """Функция обработки запросов"""
    if domain is None and dns_ip is None:
        parser = argparse.ArgumentParser(
            description="Query DNS records " "for a given domain."
        )

        parser.add_argument(
            "-U", "--url", type=str, required=True, help="URL to query DNS records for"
        )

        parser.add_argument(
            "-D",
            "--DNS",
            type=str,
            help="DNS server to use (optional). "
            "If not provided, "
            "defaults to multiple known DNS servers.",
        )
        args = parser.parse_args()

        domain = extract_domain(args.url)
        print(f"Extracted domain: {domain}")

        if args.DNS:
            dns_servers = [args.DNS]
        else:
            dns_servers = DEFAULT_DNS_SERVERS

    else:
        print(f"Extracted domain: {domain}")
        if dns_ip:
            dns_servers = [dns_ip]
        else:
            dns_servers = DEFAULT_DNS_SERVERS

    for dns_server in dns_servers:
        records = get_dns_records(domain, dns_server)
        print_dns_records(records, dns_server)


if __name__ == "__main__":
    dns_rec(None, None)
