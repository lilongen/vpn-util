#!/usr/bin/env bash

scrapy runspider spider_iprange_goog.py
scrapy runspider spider_wiki_bw.py

python3 convert_cidr_to_push_entry.py goog_cidr.yaml >> push_entrys_goog

bw_all='bw_all.csv'
bw_special='bw_special.csv'

for bw_file in ${bw_all} ${bw_special}; do
    awk -F',' '{print $3}' ${bw_file} > ${bw_file}.domain
    dig -f ${bw_file}.domain | tee  ${bw_file}.domain.dig
    grep -P -v '^(;|$)' ${bw_file}.domain.dig | grep -P '[\d+\.]{3}\.\d+$' | awk '{print substr($1,0,length($1) - 1) " " $5}' > ${bw_file}.domain.dig.pair
    awk -F' ' '{print $2}' ${bw_file}.domain.dig.pair > ${bw_file}.domain.dig.pair.ip

    final_out="push_entrys_${bw_file}"
    echo '# google ip ranges' > $final_out
    cat push_entrys_goog >> $final_out

    echo >> $final_out
    echo '# blocked websites' >> $final_out
    awk '{print "push \"route " $1 " 255.255.255.255\""}' ${bw_file}.domain.dig.pair.ip >> $final_out
done

