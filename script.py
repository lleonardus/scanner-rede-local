import csv
import nmap
import netifaces

# TODO: Automatizar escolha de interface, ou pelo menos colocar isso como um parâmetro

addrs = netifaces.ifaddresses("enp2s0")
host_ip = addrs[netifaces.AF_INET][0]["addr"]  # Ex: 192.168.0.25
nm = nmap.PortScanner()
nm.scan(
    hosts=f"{host_ip}/24", arguments="-sn", sudo=True
)  # Ping Scan (disable port scan)

with open("relatorio.csv", "w", newline="") as csvfile:
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
