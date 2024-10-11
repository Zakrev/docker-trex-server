import subprocess

def add_ip_addr(iface: str, addr: str) -> None:
    subprocess.run(["ip", "addr", "add", addr, "dev", iface], check=True)

def updown(iface: str, state: str) -> None:
    subprocess.run(["ip", "link", "set", state, iface], check=True)
