"""WebChecker"""

import sys
import importlib
from colorama import Fore, Style, init
from Dops.dns_records import dns_rec
from Dops.domain_checker import domain_check
from Dops.ssl_scanner import ssl_check
from Dops.subdomains_cheker import subdom_check
from Dops.port_scanner import scan

init(autoreset=True)
G = Fore.GREEN  # green text color
Y = Fore.YELLOW  # yellow text color
C = Fore.CYAN  # cyan text color
SB = Style.BRIGHT  # bright text style


def load_module(module_name):
    """Подгрузка функций(./Dops/)"""
    try:
        return importlib.import_module(f"Dops.{module_name}")
    except ImportError as e:
        print(Fore.RED + f"Error loading module {module_name}: {str(e)}")
        return None


def show_main_menu():
    """Генерация и отображение меню"""
    title_line_start = "=================== "
    title_line_end = " ==================="
    title_text = "Domain & Network Tools"

    end_line_start = "======= "
    end_line_end = " ========"
    end_text = "Created by @KiAtsushi | @Ki_Technologies [TG]"
    print(G + title_line_start + C + SB + title_text + G + title_line_end)
    print(Y + "[1] Domain Info Checker")
    print(Y + "[2] Port Scanner")
    print(Y + "[3] SSL Expiry Checker")
    print(Y + "[4] Subdomain Checker")
    print(Y + "[5] DNS Recorder")
    print(Y + "[0] Exit")
    print(G + end_line_start + C + SB + end_text + G + end_line_end)


def run_tool_choice(choice):
    """Поле ввода(бэкэнд), выбор функций"""
    if choice == "1":
        module = load_module("domain_checker")
        if module:
            input_text = "Enter the URL (e.g., https://example.com): "
            url = input(C + input_text)
            domain_check(url)
    elif choice == "2":
        module = load_module("port_scanner")
        if module:
            ip = input(C + "Enter the IP address to scan: ")
            start_port = input(C + "Enter the starting port: ")
            end_port = input(C + "Enter the ending port: ")
            scan(ip, start_port, end_port)
    elif choice == "3":
        module = load_module("ssl_scanner")
        if module:
            input_text = "Enter the full URL (e.g., https://dzen.ru/a/): "
            url = input(C + input_text)
            ssl_check(url)
    elif choice == "4":
        module = load_module("subdomains_cheker")
        if module:
            input_text = (
                "Enter the URL to extract the " "domain from and check subdomains: "
            )
            url = input(C + input_text)
            subdom_check(url)
    elif choice == "5":
        module = load_module("dns_records")
        if module:
            domain = input(Fore.CYAN + "Enter the domain " "to record DNS data: ")

            dns = (
                input(Fore.CYAN + "Enter the DNS server " "(leave blank for default): ")
                or None
            )
            dns_rec(domain=domain, dns_ip=dns)
    elif choice == "0":
        print(Fore.GREEN + "Exiting the program. Goodbye!")
        sys.exit(0)
    else:
        print(Fore.RED + "Invalid choice. Please select a valid option.")


def main():
    """Запуск программы"""
    while True:
        show_main_menu()
        choice = input(Fore.CYAN + "Select an option (0-5): ")

        run_tool_choice(choice)


if __name__ == "__main__":
    main()
