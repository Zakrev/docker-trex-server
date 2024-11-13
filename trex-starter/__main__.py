import pprint
import sys
from . import config, util, trex_config, firewall

def apply_ctl_port(cfg: dict, param: str, default_port: int) -> None:
    port = cfg.get(param)
    if port == None or len(port) == 0:
        return
    port = int(port)
    if port == default_port:
        return
    ip = cfg["ip"].split("/")[0]
    firewall.add_dnat(ip, port, ip, default_port, "tcp")

def apply_ctl_iface(cfg: dict) -> None:
    iface = cfg.get("iface")
    addr = cfg.get("ip")
    if iface == None or len(iface) == 0:
        return
    if addr == None or len(addr) == 0:
        return
    util.add_ip_addr(iface, addr)
    gw = cfg.get("gw")
    if gw != None and len(gw) > 0:
        util.add_default_gateway(gw)
    util.updown(iface, "up")
    apply_ctl_port(cfg, "zqm", 4500)
    apply_ctl_port(cfg, "zqm_stl", 4501)
    apply_ctl_port(cfg, "emu", 4510) # все порты за DNAT потому что в trex-сервере нельзя настроить EMU порт

def wait_ifaces(cfg: dict) -> None:
    timeout = 10
    iface = cfg["ctl"].get("iface")
    if iface:
        if False == util.wait_iface(iface, timeout):
            raise Exception("Can't wait iface " + iface)
    for iface in cfg["src"]:
        iface = iface.get("iface")
        if None == iface:
            continue
        if False == util.wait_iface(iface, timeout):
            raise Exception("Can't wait iface " + iface)
    for iface in cfg["dst"]:
        iface = iface.get("iface")
        if None == iface:
            continue
        if False == util.wait_iface(iface, timeout):
            raise Exception("Can't wait iface " + iface)

def generate_starter(cfg: dict) -> None:
    with open(sys.argv[1], "w", encoding="utf-8") as file:
        print("#!/bin/bash\n", file=file)
        if not cfg["shell"]:
            print("exec", file=file, end=" ")
        print("./t-rex-64 -i " + cfg["mode"], file=file, end=" ")
        learn_mode = cfg.get("learn_mode")
        if learn_mode:
            print("--learn-mode " + learn_mode, file=file, end=" ")
        if cfg["shell"]:
            print("1>/dev/null &\nexec bash", file=file)
        else:
            print("\n", file=file)

if __name__ == "__main__":
    cfg = config.parse_from_env()
    print("CONFIG:")
    pprint.pprint(cfg)
    wait_ifaces(cfg)
    apply_ctl_iface(cfg["ctl"])
    trex_config.generate_yml(cfg)
    generate_starter(cfg)
