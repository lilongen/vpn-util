#!/usr/bin/env bash

scrapy runspider spider_iprange_goog.py
scrapy runspider spider_wiki_bw.py

bw_file='wiki_bw.csv'
awk -F',' '{print $3}' ${bw_file} > ${bw_file}.domain

#exit 0

dig -f ${bw_file}.domain | tee  ${bw_file}.domain.dig
ggrep -P -v '^(;|$)' ${bw_file}.domain.dig | ggrep -P '[\d+\.]{3}\.\d+$' | awk '{print substr($1,0,length($1) - 1) " " $5}' > ${bw_file}.domain.dig.pair

awk -F' ' '{print $2}' ${bw_file}.domain.dig.pair > ${bw_file}.domain.dig.pair.ip

final_out='push_entrys'
echo '# google ip ranges' > $final_out
python3 convert_cidr_to_push_entry.py goog_cidr.yaml >> $final_out

echo >> $final_out
echo '# blocked websites' >> $final_out
awk '{print "push \"route " $1 " 255.255.255.255\""}' ${bw_file}.domain.dig.pair.ip >> $final_out
