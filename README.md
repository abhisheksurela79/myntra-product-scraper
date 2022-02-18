# myntra-product-scraper
A Python wrapper on myntra's private API to scrape specific product data


I wrote this to access myntra's API and scrape publically availabe data without using any 3rd party dependencies like selenium.

<h2>Usage</h2>
<br />

```python
from FetchedData import product

url = "https://www.myntra.com/sweatshirts/hm/hm-men-white-solid-cotton-hoodie/13503944/buy"  # product link
print(product(url))
