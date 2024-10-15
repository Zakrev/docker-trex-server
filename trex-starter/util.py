import subprocess

def add_ip_addr(iface: str, addr: str) -> None:
    subprocess.run(["ip", "addr", "add", addr, "dev", iface], check=True)

def updown(iface: str, state: str) -> None:
    subprocess.run(["ip", "link", "set", state, iface], check=True)

def add_default_gateway(gw: str) -> None:
    subprocess.run(["ip", "route", "add", "0.0.0.0/0", "via", gw], check=True)
