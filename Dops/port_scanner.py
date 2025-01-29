"""Port scanner"""

import asyncio
import time
import argparse


async def scan_port(ip, port):
    """Поиск открытых портов"""
    try:
        _, writer = await asyncio.open_connection(ip, port)
        print(f"[+] {port}")
        writer.close()
        await writer.wait_closed()
    except (asyncio.TimeoutError, OSError, ConnectionRefusedError):
        pass


async def scan_ports(ip, start_port, end_port):
    """Сканирование портов"""
    tasks = []
    for port in range(start_port, end_port + 1):
        tasks.append(scan_port(ip, port))

    await asyncio.gather(*tasks)


def scan(ip=None, start_port=None, end_port=None):
    """Основная функция обработки запросов"""
    if ip is None or start_port is None or end_port is None:
        parser = argparse.ArgumentParser(
            description="Port scanner for checking a range of ports."
        )
        parser.add_argument("-IP", "--ip", required=True, help="IP address to scan")
        parser.add_argument(
            "-P", "--ports", required=True, help="Port range (e.g., 1-100)"
        )
        args = parser.parse_args()

        ip = args.ip
        start_port, end_port = map(int, args.ports.split("-"))
    else:
        start_port, end_port = int(start_port), int(end_port)

    start_time = time.time()

    asyncio.run(scan_ports(ip, start_port, end_port))

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nTime taken for scan: {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    scan()
