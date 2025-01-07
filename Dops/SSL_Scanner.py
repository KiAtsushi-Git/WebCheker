import ssl
import socket
import certifi
from urllib.parse import urlparse
from datetime import datetime
import argparse


def extract_hostname(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname


def check_ssl_expiry(hostname, port=443):
    context = ssl.create_default_context(cafile=certifi.where())
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

                expiry_date_str = cert.get('notAfter', '')
                try:
                    expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y GMT')
                except ValueError:
                    expiry_date = None

                output = []
                if expiry_date:
                    output.append(f"Certificate for {hostname} expires on {expiry_date}")
                    days_remaining = (expiry_date - datetime.utcnow()).days
                    output.append(f"Days remaining until expiration: {days_remaining}")
                else:
                    output.append(f"Unable to parse the expiration date.")

                output.append("\nCertificate Information:")
                for key, value in cert.items():
                    output.append(f"{key}: {value}")

                return "\n".join(output)
    except Exception as e:
        return f"Error checking certificate: {e}"


def print_ssl_info(hostname, ssl_info):
    print(f"\nSSL Information for {hostname}:")
    print(ssl_info)


def SSL_Check(url=None):
    if url is None:
        parser = argparse.ArgumentParser(description="SSL Certificate Expiry Checker")
        parser.add_argument('-U', '--URL', required=True, help="Enter the full URL (e.g., https://dzen.ru/a/)")
        args = parser.parse_args()
        url = args.URL

    hostname = extract_hostname(url)

    if hostname:
        print(f"Extracted hostname: {hostname}")
        ssl_info = check_ssl_expiry(hostname)
        print_ssl_info(hostname, ssl_info)
    else:
        print("Unable to extract hostname from the URL.")


if __name__ == "__main__":
    SSL_Check()
