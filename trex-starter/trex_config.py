import yaml

def __fill_port_info(info: list, cfg: list) -> None:
    skip_keys = ["iface"]
    for iface in cfg:
        entry = dict()
        for key in iface.keys():
            if key in skip_keys:
                continue
            try:
                val = iface[key]
                if str.isdigit(val):
                    entry[key] = int(val)
                else:
                    entry[key] = val
            except:
                pass
        if len(entry) == 0:
            continue
        info.append(entry)

def generate_yml(cfg: dict) -> None:
    # https://trex-tgn.cisco.com/trex/doc/trex_manual.html
    config = { "version": 2 }
    interfaces = list()
    if len(cfg["src"]) != len(cfg["dst"]):
        raise Exception("Invalid configuration")
    ports_per_side = len(cfg["src"])
    for i in range(0, ports_per_side):
        interfaces.append(cfg["src"][i]["iface"])
        interfaces.append(cfg["dst"][i]["iface"])
    config["port_limit"] = len(interfaces)
    config["interfaces"] = interfaces
    src_port_info = list()
    __fill_port_info(src_port_info, cfg["src"])
    dst_port_info = list()
    __fill_port_info(dst_port_info, cfg["dst"])
    if len(src_port_info) != len(dst_port_info):
        raise Exception("Invalid configuration")
    if len(src_port_info) != ports_per_side:
        raise Exception("Invalid configuration")
    port_info = list()
    for i in range(0, ports_per_side):
        port_info.append(src_port_info[i])
        port_info.append(dst_port_info[i])
    config["port_info"] = port_info
    with open(cfg["file"], "w", encoding="utf-8") as file:
        yaml.dump([config], file)
