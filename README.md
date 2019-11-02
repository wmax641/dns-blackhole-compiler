## dns-blackhole-compiler
A helper list to generate a hostfile of blackholed hostnames. Outputs the blackholed hostnames into a hostfile that can be used locally

Can also output to dnsmasq.conf format with `-d`, and be used with dnsmasq for blocking certain domains. See below section on dnsmasq

## Usage

#### Basic local hosts file
Default with no options will pull from a preconfigured list of blacklist found from https://firebog.net/

The output will then be placed into a file called `hosts.blackholed` (default filename)
```
$ python3 dns-blackhole-compiler.py 
...
...
$ head hosts.blackholed
127.0.0.1 activmaxis.com
127.0.0.1 przyspiesz.pl
127.0.0.1 www.dailytrendsng.com
127.0.0.1 serwislaptopowwarszawa.com.pl
...
```

#### Custom lists and filenames
Default output filename: `hosts.blackholed`

The `-i/--input FILENAME` option loads the blacklist list from a local file

 The `-o/--output FILENMAE` writes the blacklist to another filename instead of the default
```
$ python3 dns-blackhole-compiler.py --input example_bl_list.txt --output hosts.txt
Opening blacklist-list file at:
   example_bl_list.txt
(1/3) Requesting blacklist at:
   https://hosts-file.net/grm.txt
   Got 534 hostnames to add to blacklist
(2/3) Requesting blacklist at:
   https://reddestdream.github.io/Projects/MinimalHosts/etc/MinimalHostsBlocker/minimalhosts
   Got 715 hostnames to add to blacklist
(3/3) Requesting blacklist at:
   https://raw.githubusercontent.com/StevenBlack/hosts/master/data/KADhosts/hosts
   Got 1647 hostnames to add to blacklist
Opening hosts.txt
   Wrote 2782 hostname blackholes
```

#### dnsmasq output
The `-d/--dnsmasq` will output to a format suitable for dnsmasq.conf, taking care to skip some unsupported hostname formats...

The below file will return NXDOMAIN for these blacklisted DNS names
```
$ python3 dns-blackhole-compiler.py -d
...
...
$ head hosts.blackholed 
address=/mkt5178.com/
address=/www.clicktrace.info/
address=/ezinetracking.com/
address=/oas.deejay.it/
...
```

#### Sample dnsmasq setup
Sample dnsmasq setup.

* Compile list of blacklists to block advertising and tracking. Sample list included in repo from https://firebog.net 
* `python3 dns-blockhole-compiler.py -d -i advertising_tracking_blacklist.txt -o dnsmasq.blacklist.conf`
* Move `dnsmasq.blacklist.conf` to `/etc/dnsmasq.d/`. May need to create the directory
* Configure dnsmasq.conf with:
```
interface=lo
listen-address=127.0.0.1
cache-size=1000
no-resolv
server=1.1.1.1
#server=8.8.8.8
conf-dir=/etc/dnsmasq.d
```
* `systemctl enable dnsmasq`
* `systemctl start dnsmasq`

Then modify `/etc/resolv.conf` either manually or via resolvectl to start directing DNS queries to `127.0.0.1`
