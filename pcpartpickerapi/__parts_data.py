"""
See the explanation comment in part_lists.get_list
as to what exactly this dictionary is used for
"""

part_lookup = {
    "cpu": {
        5: "speed",
        7: "cores",
        9: "tdp"
    },
    "cpu-cooler": {
        5: "fan-rpm",
        7: "noise-level"
    },
    "motherboard": {
        5: "socket",
        7: "form-factor",
        9: "ram-slots",
        11: "max-ram"
    },
    "memory": {
        5: "speed",
        7: "type",
        9: "cas-latency",
        11: "modules",
        13: "price/gb"
    },
    "internal-hard-drive": {
        5: "series",
        7: "form",
        9: "type",
        11: "capacity",
        13: "cache",
        15: "price/gb",
    },
    "video-card": {
        5: "series",
        7: "chipset",
        9: "memory",
        11: "core-clock"
    },
    "power-supply": {
        5: "series",
        7: "form",
        9: "efficiency",
        11: "watts",
        13: "modular",
    },
    "case": {
        5: "type",
        7: "ext525b",  # EXTERNAL 5.25" BAYS
        9: "int35b",  # INTERNAL 3.5"BAYS
        11: "power-supply",
    },
    "case-fan": {
        5: "color",
        7: "size",
        9: "rpm",
        11: "airflow",
        13: "noise-level"
    },
    "fan-controller": {
        5: "form-factor",
        7: "channels",
        9: "channel-wattage"
    },
    "thermal-paste": {
        5: "amount"
    },
    "optical-drive": {
        5: "bd",
        7: "dvd",
        9: "cd"
    },
    "sound-card": {
        5: "chipset",
        7: "channels",
        9: "bits",
        11: "snr",
        13: "sample-rate",
    },
    "wired-network-card": {
        5: "interface",
        7: "ports"
    },
    "wireless-network-card": {
        5: "interface",
        7: "protocols"
    },
    "monitor": {
        5: "resolution",
        7: "size",
        9: "response-time",
        11: "ips",
        13: "refresh-rate",
    },
    "external-hard-drive": {
        5: "series",
        7: "type",
        9: "capacity",
        11: "price/gb"
    },
    "headphones": {
        5: "type",
        7: "microphone",
        9: "wireless",
        11: "frequency-response"
    },
    "keyboard": {
        5: "style",
        7: "color",
        9: "switch-type",
        11: "backlit"
    },
    "mouse": {
        5: "tracking",
        7: "connection",
        9: "color"
    },
    "speakers": {
        5: "configuration",
        7: "total-wattage",
        9: "frequency-response"
    },
    "ups": {
        5: "capacity-w",
        7: "capacity-va"
    },   
}
