#!/usr/bin/python3

import requests
import sys
import os
import argparse

# Blacklists Consolidated List
# This is default lookup unless you use -i and specify a file with a list of URLs
BLACKLIST_LIST_URL = "https://v.firebog.net/hosts/lists.php?type=tick"

# Default ip.addr i host
BLACKHOLE_IPADDR = "127.0.0.1"

# Output filename. By default writes to this filename
OUTPUT_FILENAME = "hosts.blackholed"

# Blacklist set
BLACKLIST_SET = set()

# Whitelist set
WHITELIST_SET = set()

OPT_HELP_IN = "File with a list of URLS containing blacklists. If not specified, will use default Blacklist list found at this URL:\n{}".format(BLACKLIST_LIST_URL)
OPT_HELP_WHITELIST = "File with a list of substrings to match against hostnames to whitelist. Matched hostnames will not be added to blacklist. Beware, O(n^2) complexity!"
OPT_HELP_OUT = "Specify an output filename. If not specified, will use the default output filename; \"{}\"".format(OUTPUT_FILENAME)
OPT_HELP_DNSMASQ = "Output in dnsmasq.conf compatible format instead of (default) basic hosts file"

# Helper function to parse blacklists
# Skips lines starting with # and lines that are empty
# Pass in list, returns list, split by whitespace, if possible
def process_blacklist(hostfile):

    for line in hostfile:

        # remove leading whitespace
        line_lstrip = line.lstrip() 

        # skip (near) empty) lines
        if len(line_lstrip) <= 1:
            continue
        # comments
        elif line_lstrip[0] == "#":
            continue

        # Try try to split by whitespace, there may be 2 different results;
        #   "127.0.0.1 evil.host.io" -> ["127.0.0.1", "evil.host.io"], len = 2
        #   "another.evil.host" -> ["another.evil.host"], len = 1
        split = line_lstrip.split()
        if len(split) == 2:
            BLACKLIST_SET.add(split[1])    
        elif len(split) == 1:
            BLACKLIST_SET.add(split[0])    


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help=OPT_HELP_IN)
    parser.add_argument("-w", "--whitelist", type=str, help=OPT_HELP_WHITELIST)
    parser.add_argument("-o", "--output", type=str, help=OPT_HELP_OUT)
    parser.add_argument("-d", "--dnsmasq", action='store_true', help=OPT_HELP_DNSMASQ)
    args = parser.parse_args()

    # if defined, get blacklist list from .txt file
    if args.input: 
        print("Opening blacklist-list file at:")
        print("   {}".format(args.input))
        with open(args.input, 'r') as f:
            content = f.readlines()
        blacklists = [x.strip() for x in content]
            
    # Otherwise, use default that's online at the URL defined by BLACKLIST_LIST_URL
    else:
        try:
            print("Requesting blacklist-list at:")
            print("   {}".format(BLACKLIST_LIST_URL))
            r = requests.get(BLACKLIST_LIST_URL)
            if r.status_code != 200:
                raise Exception("Status code - {}".format(r.status_code))
        except Exception as e:
            print("Caught exception - {}".format(str(e)))
            print("Exiting....")
            sys.exit(1)

        blacklists = r.text.splitlines()

    i = 1
    for url in blacklists:
        try:
            print("({}/{}) Requesting blacklist at:".format(i, len(blacklists)))
            print("   {}".format(url))
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception("Status code - {}".format(r.status_code))
        except Exception as e:
            print("   Caught exception - {}".format(str(e)))
            print("   Exiting....")
            sys.exit(1)
        
        hostname_list = r.text.splitlines()
        print("   Got {} hostnames to add to blacklist".format(len(hostname_list)))
    
        # Read the hostname list returned, and add to blacklist
        process_blacklist(hostname_list)
        
        i += 1

    # Write blacklist to file
    if args.output:
        filename = args.output
    else:
        filename = OUTPUT_FILENAME
    print("Opening {}".format(filename))

    i = 0
    with open(filename, 'w') as f:
        for hostname in BLACKLIST_SET:
            # dnsmasq config file format
            if args.dnsmasq:
                # Skip some hostnames that dnsmasq doesn't support
                if "--" in hostname:
                    continue
                elif hostname.startswith("-"):
                    continue
                f.write('address=/{}/{}\n'.format(hostname, BLACKHOLE_IPADDR))
            # default, hostfile format (eg. 127.0.0.1 hostname)
            else:
                f.write('{} {}\n'.format(BLACKHOLE_IPADDR, hostname))
            i += 1
    print("   Wrote {} hostname blackholes".format(i))
