part_type_column_names = {
    "cpu": ["speed", "cores", "tdp"],
    "cpu-cooler": ["fan-rpm", "noise-level"],
    "motherboard": ["socket", "form-factor", "ram-slots", "max-ram"],
    "memory": ["speed", "type", "cas-latency", "modules", "price/gb"],
    "internal-hard-drive": ["series", "form", "type", "capacity", "cache", "price/gb"],
    "video-card": ["series", "chipset", "memory", "core-clock"],
    "power-supply": ["series", "form", "efficiency", "watts", "modular"],
    "case": ["type", "ext525b", "int35b", "power-supply"],
    "case-fan": ["color", "size", "rpm", "airflow", "noise-level"],
    "fan-controller": ["form-factor", "channels", "channel-wattage"],
    "thermal-paste": ["amount"],
    "optical-drive": ["bd", "dvd", "cd"],
    "sound-card": ["chipset", "channels", "bits", "snr", "sample-rate"],
    "wired-network-card": ["interface", "ports"],
    "wireless-network-card": ["interface", "protocols"],
    "monitor": ["resolution", "size", "response-time", "ips", "refresh-rate"],
    "external-hard-drive": ["series", "type", "capacity", "price/gb"],
    "headphones": ["type", "microphone", "wireless", "frequency-response"],
    "keyboard": ["style", "color", "switch-type", "backlit"],
    "mouse": ["tracking", "connection", "color"],
    "speakers": ["configuration", "total-wattage", "frequency-response"],
    "ups": ["capacity-w", "capacity-va"],
}

# Every part_type has these columns, no need to write them all out by hand
for col_name in part_type_column_names:
    part_type_column_names[col_name].insert(0, "name")
    part_type_column_names[col_name].append("ratings_count")
    part_type_column_names[col_name].append("price")
