import scrapy

class AmazonBooks(scrapy.Spider):
    name = 'amazonbooks'
    start_urls = ["https://www.amazon.com/charts/"]

    def parse(self, response):
        to_csv = True

        if not to_csv:
            #########################
            ### Export to Console ###
            #########################

            for rank in response.css('.kc-rank-card-rank'):
                rank_text = rank.select("text()").extract()[0].strip()
                yield {'rank': rank_text}

            for title in response.css('.kc-rank-card-title'):
                title_text = title.select("text()").extract()[0].strip()
                yield {'title': title_text}

            for author in response.css('.kc-rank-card-author'):
                author_text = author.select("text()").extract()[0].strip()
                yield {'author': author_text}

        else:
            #####################
            ### Export to CSV ###
            #####################

            # make sure output.csv doesn't already exist!
            file = open("output.csv", "a+")

            headers = ["rank, title, author"]
            file.write("{}\n".format(','.join(header for header in headers)))

            ranks = response.css('.kc-rank-card-rank')
            titles = response.css('.kc-rank-card-title')
            authors = response.css('.kc-rank-card-author')

            # for some reason ranks is doubled, oh well
            for i in range(len(ranks)):
                fields = []

                rank = ranks[i]
                rank_text = rank.select("text()").extract()[0].strip()
                fields.append(rank_text)

                title = titles[i]
                title_text = title.select("text()").extract()[0].strip()
                fields.append(title_text)

                author = authors[i]
                author_text = author.select("text()").extract()[0].strip()
                fields.append(author_text)

                file.write("{}\n".format(','.join(str(field) for field in fields)))

spider = AmazonBooks()
spider.parse
