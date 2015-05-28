#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:04:37 2015

@author: nad2000
"""

from collections import defaultdict
import re

import argparse
import os
import time

from matplotlib import pyplot as plt
import pandas as pn
#%%

default_data_file = 'top.log'

parser = argparse.ArgumentParser(description='Parse and generate out put of collect_data.sh')
parser.add_argument('input', nargs='?', type=str, help='collect_data.sh input file (default: {0})'.format(default_data_file), default=default_data_file)
##parser.add_argument('-t', '--terminate', type=int, default=3600, help='Stop transmitting after <n> seconds (default: 1 hour)')

args = parser.parse_args()


#%%

ts0 = ts = 0
d = defaultdict(int)
apps = set()

with open(args.input) as f:
    for line in f:
        #print line
        if not ts:
            if line.startswith("14"):  # line with the timestamp
                ts = int(line.strip())
                if ts0 == 0:
                    ts0 = ts
            continue
        if line.startswith("+++"):
            if d:
                pass
                ##print "===", ts
                ##for k, v in sorted(d.items(), key=lambda x: -x[1]):
                ##    print k, ":", v, "%d" % (v/1000)
            #d = defaultdict(int)
            ts = 0
            continue
        if d != 0:
            vals  = re.split("\ *", line.strip())
            if len(vals) < 7:
                continue
            pid, user, cpu, rss, vsz, comm = vals[:6]
            if comm != "CMD" and rss != "0":
                d[(ts,comm)] += int(rss)
                apps.add(comm)

#%%
def rssval(ts, conn):
    if ts == ts0:
        return 0
    else:
        if d[(ts, conn)] == 0:
            return rssval(ts-1, conn)
        else:
            return d[(ts, conn)]
#%%

apps = sorted(apps)
#%%

app_max = dict(((a, max((d[(t,a)] for t in xrange(ts0, ts)))) for a in apps))
app_max = sorted(app_max.items(), key=lambda i: -i[1])
top7_app = [a for (a, _) in app_max[:7]]
for (t, a) in d.keys()[:]:
    if a not in top7_app:
        d[(t, 'OTHER')] += d[(t, a)]
        

#%%
ts_range = range(ts0 + 1, ts + 1)

#%%
apps_short = top7_app + ['OTHER']

# Print as CSV:
##print ","+",".join(apps_short)
##for t in ts_range:
##    print str(t) + "," +  ",".join([str(rssval(t,conn)) for conn in apps_short])


#%%

dd = pn.DataFrame(columns=apps_short, index=ts_range)
for a in apps_short:
    dd[a] = pn.Series( (rssval(t,a) for t in ts_range), index=ts_range)


#%%
fig, axs = plt.subplots(2,1)
dd.plot(kind="area", ax=axs[0] )
dd.plot(kind="area", stacked=False, ax=axs[1] )
plt.show()

#%%


