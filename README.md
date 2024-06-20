# mercadolibre-scraper

Scrape MercadoLibre search results and product pages.

## Installation

### Setup
1. Clone the repository 
```
git clone https://github.com/XavierZambrano/mercadolibre-scraper.git
```
2. Create a virtual environment and activate it
3. Install the requirements
```bash
pip install -r requirements.txt
```

### Usage
```
scrapy crawl mercadolibre -a query="search query" -a country="country code" -O output.csv
```
For more information about scrapy crawl arguments, check the [Scrapy documentation](https://docs.scrapy.org/en/latest/topics/commands.html#std-command-crawl).

[Example result](assets/sombrilla.csv)


### Notes
- In the variable `data` exists a lot of data, I've only used a small part of it. If you want extract more data, check the `data` variable, [example data variable value](test/mercadolibre_MLM24566773.json).
- The scraper is not perfect, was created in a few hours and lacks of tests.
