
## 专利数据爬虫

最近在抓专利数据，研究了介个专利数据的网站，中国专利公布公告, soopat, 还有就只这次的重点，CNKI中国知网的专利数据，由于soonpat有验证码, 中国专利公布公告的反爬页很严重，最后就重点做了知网的专利数据

知网的专利数据还算比较好抓，但是要注意它的url结构，这里给大家开源一个使用selenium来抓取的代码，另外直接使用requests抓取的页基本上要完成了，但是还是逃不过７页必死的魔咒，最后就转换思路，将搜索条件缩小，抓取每个分类下的每一天的数据，基本上不会出现超过７页的情况，基本满足了需求

