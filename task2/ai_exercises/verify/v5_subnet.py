import ipaddress
net = ipaddress.ip_network("192.168.10.0/24")
for s in net.subnets(new_prefix=26):
    hosts = list(s.hosts())
    print(f"{s}  mask {s.netmask}  first {hosts[0]}  last {hosts[-1]}  broadcast {s.broadcast_address}  usable {len(hosts)}")
