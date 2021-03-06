# scrapy wikipedia blocked websites
#
import scrapy


class WikiBWSpider(scrapy.Spider):
    name = 'wiki-spider'

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_websites_blocked_in_mainland_China'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = f'{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        trs = response.xpath('//table[contains(@class, "wikitable")]//tr')
        lines = ''
        for tr in trs:
            site = tr.xpath('td[2]//text()').extract_first()
            domain = tr.xpath('td[3]//text()').extract_first()
            url = tr.xpath('td[4]//text()').extract_first()
            lines += f'{site},{domain},{url}\n'

        self.log(lines)
        with open('bw_all.csv', 'w') as bw_file:
            bw_file.write(lines)
