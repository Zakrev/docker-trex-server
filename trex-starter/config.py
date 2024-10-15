import os

def __create_node(cfg: dict, tree: list) -> set:
    i = 0
    while i < len(tree) - 1:
        entry = cfg.get(tree[i])
        if entry == None:
            entry = dict()
            cfg[tree[i]] = entry
        cfg = entry
        i += 1
    return (cfg, tree[i])

def __pars_val(cfg: dict, tree: list, val: str, entry: dict):
    cfg,param = __create_node(cfg, tree)
    cfg[param] = val

def __pars_srcdst_iface_param(cfg: dict, tree: list, val: str, entry: dict):
    direction = tree[0]
    param = tree[1]
    val = val.split(" ")
    idx = 0
    for value in val:
        try:
            iface = cfg[direction][idx]
            iface[param] = value
        except:
            iface = { param: value }
            cfg[direction].append(iface)
        idx += 1

def __pars_keyword(cfg: dict, tree: list, val: str, entry: dict):
    cfg,param = __create_node(cfg, tree)
    cfg[param] = entry["keywords"][val]

__bool = {
    "Y": True,
    "N": False,
}

__mode = {
    "STL": "--stl",
    "ASTF": "--astf",
    "EMU": "--emu",
}

__keys = {
    "FILE": {"tree": ["file"]},
    "SHELL": {"func": __pars_keyword, "keywords": __bool, "tree": ["shell"]},
    "MODE": {"func": __pars_keyword, "keywords": __mode, "tree": ["mode"]},
    "LEARN_MODE": {"tree": ["learn_mode"]},
    "CTL_IFACE": {"tree": ["ctl", "iface"]},
    "CTL_IFACE_IP": {"tree": ["ctl", "ip"]},
    "CTL_IFACE_GW": {"tree": ["ctl", "gw"]},
    "CTL_ZQM": {"tree": ["ctl", "zqm"]},
    "CTL_ZQM_STL": {"tree": ["ctl", "zqm_stl"]},
    "CTL_EMU": {"tree": ["ctl", "emu"]},
    "SRC_IFACE": {"func": __pars_srcdst_iface_param, "tree": ["src", "iface"]},
    "SRC_IFACE_VLAN": {"func": __pars_srcdst_iface_param, "tree": ["src", "vlan"]},
    "SRC_IFACE_MAC": {"func": __pars_srcdst_iface_param, "tree": ["src", "src_mac"]},
    "SRC_IFACE_IP": {"func": __pars_srcdst_iface_param, "tree": ["src", "ip"]},
    "SRC_IFACE_GW": {"func": __pars_srcdst_iface_param, "tree": ["src", "default_gw"]},
    "SRC_IFACE_DST_MAC": {"func": __pars_srcdst_iface_param, "tree": ["src", "dst_mac"]},
    "DST_IFACE": {"func": __pars_srcdst_iface_param, "tree": ["dst", "iface"]},
    "DST_IFACE_VLAN": {"func": __pars_srcdst_iface_param, "tree": ["dst", "vlan"]},
    "DST_IFACE_MAC": {"func": __pars_srcdst_iface_param, "tree": ["dst", "src_mac"]},
    "DST_IFACE_IP": {"func": __pars_srcdst_iface_param, "tree": ["dst", "ip"]},
    "DST_IFACE_GW": {"func": __pars_srcdst_iface_param, "tree": ["dst", "default_gw"]},
    "DST_IFACE_DST_MAC": {"func": __pars_srcdst_iface_param, "tree": ["dst", "dst_mac"]},
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
        tree = __keys[key].get("tree")
        func = __keys[key].get("func", __pars_val)
        func(config, tree, os.environ[var], __keys[key])
    return config
