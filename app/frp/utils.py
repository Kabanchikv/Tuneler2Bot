import os
from .config import settings

def generate_frp_config(subdomain: str) -> str:
    """Генерирует конфиг FRP в формате TOML"""
    return f"""[common]
server_addr = "{settings.FRP_SERVER_ADDR}"
server_port = {settings.FRP_SERVER_PORT}

[{subdomain}]
type = http
local_port = 8080
custom_domains = "{subdomain}.{settings.FRP_DOMAIN}"
"""

def save_toml_file(subdomain: str, config: str) -> str:
    """Сохраняет конфиг в файл .toml"""
    filename = f"{subdomain}.toml"
    with open(filename, 'w') as f:
        f.write(config)
    return filename