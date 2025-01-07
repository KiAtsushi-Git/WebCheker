import sys
import importlib
from colorama import Fore, Style, init
from Dops.DNS_Records import DNS_Rec
from Dops.Domain_Cheker import Domain_Check
from Dops.SSL_Scanner import SSL_Check
from Dops.SubDomains_Cheker import SubDom_Check
from Dops.Port_Scanner import scan

init(autoreset=True)

def load_module(module_name):
    try:
        return importlib.import_module(f"Dops.{module_name}")
    except ImportError as e:
        print(Fore.RED + f"Error loading module {module_name}: {str(e)}")
        return None

def show_main_menu():
    print(Fore.GREEN + "=================== " + Fore.CYAN + Style.BRIGHT + "Domain & Network Tools" + Fore.GREEN + " ===================")
    print(Fore.YELLOW + "[1] Domain Info Checker")
    print(Fore.YELLOW + "[2] Port Scanner")
    print(Fore.YELLOW + "[3] SSL Expiry Checker")
    print(Fore.YELLOW + "[4] Subdomain Checker")
    print(Fore.YELLOW + "[5] DNS Recorder")
    print(Fore.YELLOW + "[0] Exit")
    print(Fore.GREEN + "======= " + Fore.CYAN + Style.BRIGHT + "Created by @KiAtsushi | @Ki_Technologies [TG]" + Fore.GREEN + " ========")

def run_tool_choice(choice):
    if choice == '1':
        module = load_module('Domain_Cheker')
        if module:
            url = input(Fore.CYAN + "Enter the URL (e.g., https://example.com): ")
            Domain_Check(url)
    elif choice == '2':
        module = load_module('Port_Scanner')
        if module:
            ip = input(Fore.CYAN + "Enter the IP address to scan: ")
            start_port = input(Fore.CYAN + "Enter the starting port: ")
            end_port = input(Fore.CYAN + "Enter the ending port: ")
            scan(ip, start_port, end_port)
    elif choice == '3':
        module = load_module('SSL_Scanner')
        if module:
            url = input(Fore.CYAN + "Enter the full URL (e.g., https://dzen.ru/a/): ")
            SSL_Check(url)
    elif choice == '4':
        module = load_module('SubDomains_Cheker')
        if module:
            url = input(Fore.CYAN + "Enter the URL to extract the domain from and check subdomains: ")
            SubDom_Check(url)
    elif choice == '5':
        module = load_module('DNS_Records')
        if module:
            domain = input(Fore.CYAN + "Enter the domain to record DNS data: ")
            dns = input(Fore.CYAN + "Enter the DNS server (leave blank for default): ") or None
            DNS_Rec(domain=domain, dns=dns)
    elif choice == '0':
        print(Fore.GREEN + "Exiting the program. Goodbye!")
        sys.exit(0)
    else:
        print(Fore.RED + "Invalid choice. Please select a valid option.")

def main():
    while True:
        show_main_menu()
        choice = input(Fore.CYAN + "Select an option (0-5): ")

        run_tool_choice(choice)

if __name__ == "__main__":
    main()
