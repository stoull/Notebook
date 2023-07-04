# Bonjour and mDNS

Can I list all the Bonjour-enabled services that are running?

`dns-sd` 命令

Running `dns-sd -B _services._dns-sd._udp` will return a list of all available service types that currently being advertised. 


[Bonjour手把手搭建一：mDNS（apple & multicastdns.org）](https://blog.csdn.net/ScarletMeCarzy/article/details/106544095)


[How to find all devices (IP Address, Hostname, MAC Address) on local network?](https://apple.stackexchange.com/questions/310061/how-to-find-all-devices-ip-address-hostname-mac-address-on-local-network)

`arp-scan` (available via Homebrew)

`brew install arp-scan`
`arp-scan --localnet`