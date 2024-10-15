import subprocess

def add_dnat(ip: str, port: int, nat: str, pat: int, proto: str) -> None:
    port = str(port)
    pat = str(pat)
    subprocess.run(["iptables", "-t", "nat", "-A", "PREROUTING", "-d", ip, "-p", proto, "--dport", port, "-j", "DNAT", "--to-destination", nat + ":" + pat], check=True)
    subprocess.run(["iptables", "-t", "nat", "-A", "POSTROUTING", "-d", nat, "-p", proto, "--dport", pat, "-j", "MASQUERADE"], check=True)
