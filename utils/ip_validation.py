import ipaddress


def validate_ip(ip_address: str):
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        raise ValueError("Invalid IP address format.")
