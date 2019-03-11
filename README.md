## dns-blackhole-compiler
A helper list to generate a hostfile of blackholed hostnames

## Usage

Default with no options will pull from a preconfigured list of blacklist found from https://firebog.net/

The output will then be placed into a file called `hosts.blackholed`
```
$ python3 dns-blackhole-compiler.py 
...
...
$ head hosts.blackholed
127.0.0.1 activmaxis.com
127.0.0.1 przyspiesz.pl
127.0.0.1 www.dailytrendsng.com
127.0.0.1 serwislaptopowwarszawa.com.pl
127.0.0.1 n4403ad.doubleclick.net
127.0.0.1 darmowe-ebooki.com.pl
127.0.0.1 feng.bu.edu.eg
127.0.0.1 www.act-natural.pl
127.0.0.1 888casino.com
127.0.0.1 vimeoo.net
```



The `-i/--input` option loads the blacklist list from a local file

 The `-o/--output` writes the blacklist to another filename instead of the default
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
