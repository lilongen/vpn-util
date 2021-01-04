import scrapy
import json
import yaml


class IprangeGoogSpider(scrapy.Spider):
    name = 'iprange-goog-spider'

    def start_requests(self):
        urls = [
            'https://www.gstatic.com/ipranges/goog.json'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_file = response.url.split("/")[-1]
        filename = f'{json_file}'
        with open(filename, 'wb') as f:
            f.write(response.body)
            ipranges = json.loads(response.body)
            self.log(f'Saved file {filename}')

        prefixes = ipranges['prefixes']
        cidr = []
        for prefix in prefixes:
            if prefix.get('ipv4Prefix') is None: break
            cidr.append(prefix.get('ipv4Prefix'))

        with open('goog_cidr.yaml', 'w') as f:
            yaml.dump(cidr, f)
