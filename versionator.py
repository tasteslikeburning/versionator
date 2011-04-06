#! /usr/bin/env python
# Jason Royes
# 3/30/2011
# Reveals the possibly hidden structure of a website by exploring hidden version control files recursively.
# Only does CVS right now.
# Optionally supports downloading of all files exposed.

import sys, os, getopt
import urllib2

download_entries = 0
overwrite = 0

def fetch_entries(base_url):
    url = base_url + "CVS/Entries"
    try:
        entries = urllib2.urlopen(url).readlines()
    except:
        print "failed to fetch entries @", url
        return
    for e in entries:
        fields = e.split('/')
        if len(fields) < 2: break
        if fields[0] == 'D':
            # make a directory
            dname = fields[1]
            print "entering directory:", dname
            if not os.path.exists(fields[1]):
                os.mkdir(dname)
            os.chdir(dname)
            fetch_entries(base_url + dname + "/")
            os.chdir('..')
        elif fields[0] == '':
            if os.path.exists(fields[1]):
                print "skipping:", fields[1]
                continue
            if download_entries:
                print "fetching file:", fields[1]
                fdata = urllib2.urlopen(base_url + fields[1]).read()
                f = open(fields[1], "w")
                f.write(fdata)
                f.close()
            else:
                f = open(fields[1], "w")
                f.close()

def usage():
    print "usage: %s [options] directory_root http://base.url.com/" %sys.argv[0]
    print "\t--download:\tActually download files found in CVS/Entries"
    print "\t--overwrite:\tOverwrite files that already exist"
    sys.exit()
    
if __name__ == "__main__":
    long_opts = [
        'download', 
        'overwrite',
    ]
    options, args = getopt.getopt(sys.argv[1:], '', long_opts)
    for ot in options:
        name, val = ot
        if name == "--download":
            download_entries = 1
        elif name == "--overwrite":
            overwrite = 1

    if len(args) < 2:
        usage()

    working_dir, url = args
    os.chdir(working_dir)
    fetch_entries(url)
