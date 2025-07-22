import nmap
import netifaces

# TODO: Automatizar escolha de interface, ou pelo menos colocar isso como um parâmetro
# TODO: Descobrir como transformar o output em um arquivo csv


def get_info():
    addrs = netifaces.ifaddresses("enp2s0")
    host_ip = addrs[netifaces.AF_INET][0]["addr"]  # Ex: 192.168.0.25
    nm = nmap.PortScanner()
    nm.scan(
        hosts=f"{host_ip}/24", arguments="-sn", sudo=True
    )  # Ping Scan (disable port scan)

    print("IP;MAC;Fabricante")
    for host in nm.all_hosts():
        if nm[host]["status"]["reason"] != "localhost-response":
            mac = nm[host]["addresses"]["mac"]
            fabricante = list(nm[host]["vendor"].values())
            print(f"{host};{mac};{fabricante[0] if len(fabricante) > 0 else None}")
        else:
            mac = addrs[netifaces.AF_LINK][0]["addr"]
            fabricante = list(nm[host]["vendor"].values())
            print(f"{host};{mac};{fabricante[0] if len(fabricante) > 0 else None}")


get_info()
