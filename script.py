import netifaces
import nmap
import csv

gws = netifaces.gateways()
default_gateway_ip = gws["default"][netifaces.AF_INET][0]
interface_name = gws["default"][netifaces.AF_INET][1]

addrs = netifaces.ifaddresses(interface_name)

nm = nmap.PortScanner()
nm.scan(hosts=f"{default_gateway_ip}/24", arguments="-sn", sudo=True)

with open(file="relatorio.csv", mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(["IP", "MAC", "Fabricante"])
    for host in nm.all_hosts():
        if nm[host]["status"]["reason"] != "localhost-response":
            mac = nm[host]["addresses"]["mac"]
            fabricante = list(nm[host]["vendor"].values())
            writer.writerow(
                [host, mac, fabricante[0] if len(fabricante) > 0 else "null"]
            )
        else:
            mac = addrs[netifaces.AF_LINK][0]["addr"].upper()
            fabricante = list(nm[host]["vendor"].values())
            writer.writerow(
                [host, mac, fabricante[0] if len(fabricante) > 0 else "null"]
            )

print("Relatório concluído e salvo em relatorio.csv")
