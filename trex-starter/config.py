import os

__mode = {
    "STL": "--stl",
    "ASTF": "--astf",
    "EMU": "--emu",
}

def __parse_file(cfg: dict, val: str):
    cfg["file"] = val

def __parse_shell(cfg: dict, val: str):
    if val == "Y":
        cfg["shell"] = True
    elif val == "N":
        cfg["shell"] = False

def __parse_mode(cfg: dict, val: str):
    cfg["mode"] = __mode[val]

def __parse_learn_mode(cfg: dict, val: str):
    cfg["learn_mode"] = val

def __parse_ctl_iface(cfg: dict, val: str):
    cfg["ctl"]["iface"] = val

def __parse_ctl_iface_ip(cfg: dict, val: str):
    cfg["ctl"]["ip"] = val

def __parse_srcdst_iface_param(cfg: dict, val: str, dir: str, param: str):
    val = val.split(" ")
    idx = 0
    for value in val:
        try:
            iface = cfg[dir][idx]
            iface[param] = value
        except:
            iface = { param: value }
            cfg[dir].append(iface)
        idx += 1

def __parse_src_iface(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "src", "iface")

def __parse_src_iface_vlan(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "src", "vlan")

def __parse_src_iface_mac(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "src", "src_mac")

def __parse_src_iface_ip(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "src", "ip")

def __parse_src_iface_gw(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "src", "default_gw")

def __parse_src_iface_dst_mac(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "src", "dst_mac")

def __parse_dst_iface(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "dst", "iface")

def __parse_dst_iface_vlan(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "dst", "vlan")

def __parse_dst_iface_mac(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "dst", "src_mac")

def __parse_dst_iface_ip(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "dst", "ip")

def __parse_dst_iface_gw(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "dst", "default_gw")

def __parse_dst_iface_dst_mac(cfg: dict, val: str):
    __parse_srcdst_iface_param(cfg, val, "dst", "dst_mac")

__keys = {
    "FILE": __parse_file,
    "SHELL": __parse_shell,
    "MODE": __parse_mode,
    "LEARN_MODE": __parse_learn_mode,
    "CTL_IFACE": __parse_ctl_iface,
    "CTL_IFACE_IP": __parse_ctl_iface_ip,
    "SRC_IFACE": __parse_src_iface,
    "SRC_IFACE_VLAN": __parse_src_iface_vlan,
    "SRC_IFACE_MAC": __parse_src_iface_mac,
    "SRC_IFACE_IP": __parse_src_iface_ip,
    "SRC_IFACE_GW": __parse_src_iface_gw,
    "SRC_IFACE_DST_MAC": __parse_src_iface_dst_mac,
    "DST_IFACE": __parse_dst_iface,
    "DST_IFACE_VLAN": __parse_dst_iface_vlan,
    "DST_IFACE_MAC": __parse_dst_iface_mac,
    "DST_IFACE_IP": __parse_dst_iface_ip,
    "DST_IFACE_GW": __parse_dst_iface_gw,
    "DST_IFACE_DST_MAC": __parse_dst_iface_dst_mac,
}

def __default_cfg() -> dict:
    return {
        "file": "/etc/trex_cfg.yaml",
        "shell": False,
        "mode": __mode["STL"],
        "ctl": {
            "iface": "eth0",
        },
        "src": [
            {
                "iface": "eth1",
            },
        ],
        "dst": [
            {
                "iface": "eth2",
            },
        ],
    }

def parse_from_env() -> dict:
    config = __default_cfg()
    for var in os.environ:
        if not var.startswith("TREX_CFG_"):
            continue
        key = var[len("TREX_CFG_"):]
        __keys[key](config, os.environ[var])
    return config
