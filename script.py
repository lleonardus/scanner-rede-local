import netifaces
import nmap
import csv

gws = netifaces.gateways()
default_gateway_ip = gws["default"][netifaces.AF_INET][0]
interface_name = gws["default"][netifaces.AF_INET][1]

addrs = netifaces.ifaddresses(interface_name)

nm = nmap.PortScanner()
nm.scan(hosts=f"{default_gateway_ip}/24", arguments="-sn", sudo=True)

with open(file="report.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file, delimiter=";")
    writer.writerow(["IP", "MAC", "Vendor"])
    for host in nm.all_hosts():
        if nm[host]["status"]["reason"] != "localhost-response":
            mac = nm[host]["addresses"]["mac"]
            vendor = list(nm[host]["vendor"].values())
            writer.writerow([host, mac, vendor[0] if len(vendor) > 0 else "Unknown"])
        else:
            mac = addrs[netifaces.AF_LINK][0]["addr"].upper()
            vendor = list(nm[host]["vendor"].values())
            writer.writerow([host, mac, vendor[0] if len(vendor) > 0 else "Unknown"])

print("Report completed and saved in report.csv")
