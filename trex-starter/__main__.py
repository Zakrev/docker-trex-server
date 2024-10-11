import pprint
import sys
from . import config, util, trex_config

def apply_ctl_iface(cfg: dict) -> None:
    iface = cfg.get("iface")
    addr = cfg.get("ip")
    if iface == None or len(iface) == 0:
        return
    if addr == None or len(addr) == 0:
        return
    util.add_ip_addr(iface, addr)
    util.updown(iface, "up")

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
    apply_ctl_iface(cfg["ctl"])
    trex_config.generate_yml(cfg)
    generate_starter(cfg)
