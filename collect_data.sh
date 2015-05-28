#!/usr/bin/sh
while true ; do  sleep 1; echo "+++" ; date ; date +%s ; ps -e -o pid,user,cpu,rss,size,comm=,cmd --sort -rss,-size ; done | grep -v "\-     0     0"
