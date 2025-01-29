"""Domain checker"""

import json
import argparse
import socket
from urllib.parse import urlparse
import whois
from whois.exceptions import WhoisException
import requests
from bs4 import BeautifulSoup


def get_ip_address(domain):
    """Поиск IP"""
    try:
        return socket.gethostbyname(domain)
    except socket.error:
        return None


def get_domain_info(domain):
    """Поиск WHOIS"""
    try:
        return whois.whois(domain)
    except WhoisException as e:
        return str(e)


def get_site_details(url):
    """Получение HTML сайта"""
    try:
        response = requests.get(url, timeout=10)
        return response.text
    except requests.RequestException as e:
        return str(e)


def parse_html(content):
    """Парсинг HTML файла"""
    soup = BeautifulSoup(content, "html.parser")
    data = {
        "title": soup.title.string if soup.title else "No title",
        "meta_description": (
            soup.find("meta", attrs={"name": "description"})["content"]
            if soup.find("meta", attrs={"name": "description"})
            else "No meta description"
        ),
        "links": [a["href"] for a in soup.find_all("a", href=True)],
        "images": [img["src"] for img in soup.find_all("img", src=True)],
        "headers": (
            {
                meta.get("name", meta.get("property")): meta.get("content")
                for meta in soup.find_all("meta", attrs={"name": True})
            }
        ),
    }
    return data


def get_ip_info(ip):
    """Поиск информации по IP"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        return response.json()
    except requests.RequestException as e:
        return str(e)


def print_info(url, ip_address, ip_info_str, domain_info_str, parsed_details):
    """Вывод найденой информации"""
    print(f"Website: {url}")
    print(f"IP Address: {ip_address}")
    print("IP Information:")
    print(ip_info_str)

    print("\nDomain Information:")
    print(domain_info_str)

    print(f"\nPage Title: {parsed_details['title']}")
    print(f"Meta Description: {parsed_details['meta_description']}")
    print(f"Links on the page: {parsed_details['links']}")
    print(f"Images on the page: {parsed_details['images']}")
    print(f"Meta Tags: {parsed_details['headers']}")

    useful_links = [
        f"Google Cache: "
        f"https://webcache.googleusercontent.com/search?q=cache:{url}",
        f"Archive.org: https://web.archive.org/web/*/{url}",
    ]
    print("\nUseful Links:")
    for link in useful_links:
        print(link)


def domain_check(url=None):
    """Основная функция обработки запросов"""
    if url is None:
        help_text = "Enter the URL (e.g., https://example.com)"
        parser = argparse.ArgumentParser(description="Domain Information Checker")
        parser.add_argument("-U", "--URL", required=True, help=help_text)
        args = parser.parse_args()
        url = args.URL

    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path

    ip_address = get_ip_address(domain)
    ip_info_str = ""
    if ip_address:
        ip_info = get_ip_info(ip_address)
        ip_info_str = json.dumps(ip_info, indent=4)

    domain_info = get_domain_info(domain)
    domain_info_str = str(domain_info)

    site_details = get_site_details(url)
    parsed_details = parse_html(site_details)

    print_info(url, ip_address, ip_info_str, domain_info_str, parsed_details)


if __name__ == "__main__":
    domain_check()
