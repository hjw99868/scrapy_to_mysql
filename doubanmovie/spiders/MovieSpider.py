# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from doubanmovie.items import DoubanmovieItem

class movieSpider(CrawlSpider):
    name="doubanmovie"
    allowed_domains=["movie.douban.com"]
    start_urls=["https://movie.douban.com/top250"]
    rules=(
        Rule(SgmlLinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*'))),
        Rule(SgmlLinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')),callback='parse_item'),      
    )

    def parse_item(self,response):
        sel=Selector(response)
        item=DoubanmovieItem()
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor']= sel.xpath('//a[@rel="v:starring"]/text()').extract()
        item['img']= sel.select('//*[@id="mainpic"]/a/img/@src').extract()
        item['num'] = sel.xpath('//*[@id="content"]/div[1]/span[1]/text()').extract()
        item['link'] = response.url
        item['commentnum'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()').extract()
        item['commentweb'] = response.url+'collection'
        storr=sel.xpath('//*[@id="link-report"]/span[1]/text()|//*[@id="link-report"]/span[1]/span/text()').extract()
        strr="".join(storr)
        item['story']=''.join(strr.split())
	return item
