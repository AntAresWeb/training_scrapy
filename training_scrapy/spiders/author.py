import scrapy


class AuthorSpider(scrapy.Spider):
    name = "author"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        # Находим все ссылки на авторов.
        all_authors = response.css('a[href^="/author/"]')
        # Перебираем ссылки по одной.
        for author_link in all_authors:
            # Здесь напишем переход по каждой из полученных ссылок,
            # чтобы спарсить страницы авторов.
            yield response.follow(author_link, callback=self.parse_author)

        # Переход по страницам пагинации (точно как в пауке quotes).
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        # Здесь будет код для парсинга страниц авторов
        # и возврат полученных данных.
        yield {
            'name': response.css('.author-title::text').get(),
            'born_date': response.css('.author-born-date::text').get(),
            'born_location': response.css('.author-born-location::text').get(),
        }
