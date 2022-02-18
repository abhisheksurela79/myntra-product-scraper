import json
import re
import requests


class InvalidInput(Exception):
    pass


class Product:
    def __init__(self, product_url: str):
        self.product_url = product_url

    def url_validation(self):
        try:
            if type(self.product_url) is str and type(int(self.product_url.split("/")[-2])):

                if "myntra.com" in re.findall('://www.([\w\-\.]+)', self.product_url):
                    pass

                else:
                    raise InvalidInput("Provided input is not Myntra's product link")

        except Exception as e:
            raise InvalidInput(e)

    def fetch_data(self):
        from Headers import fetched_header
        self.url_validation()

        product_code = self.product_url.split("/")[-2]

        url = f"https://www.myntra.com/gateway/v2/product/{product_code}"
        fetched_header = fetched_header()

        response = requests.request("GET", url, cookies=fetched_header['cookies'],
                                    headers=fetched_header['headers'], data=fetched_header['payload'])

        raw_data = json.loads(response.text)

        product_name = raw_data['style']['brand']['name']
        image = raw_data['style']['media']['albums'][0]['images'][0]['src']
        to_replace = [["($height)", "732"], ["($qualityPercentage)", "90"], ["($width)", "600"]]

        # Resizing  product image to save network bandwidth
        for _ in range(3):
            image = image.replace(to_replace[_][0], to_replace[_][1])

        # print(raw_data)

        discounted_price = "None"
        mrp = raw_data['style']['mrp']

        for i in raw_data['style']['sizes']:
            if "sizeSellerData" in i:
                for j in i['sizeSellerData']:
                    if "discountedPrice" in j:
                        discounted_price = j['discountedPrice']
                        break

        available_count = 0

        for total in raw_data['style']['sizes']:
            if "sizeSellerData" in total:
                for each in total['sizeSellerData']:
                    if "availableCount" in each:
                        available_count += each['availableCount']

        # If encountered a product with no rating, handling with exception
        try:
            average_rating = raw_data['style']['ratings']['averageRating']
        except TypeError:
            average_rating = "None"

        return json.dumps(
            {'product_name': product_name, "image": image, "discounted_Price": discounted_price, "MRP": mrp,
             "available_Count": available_count, "average_Rating": format(average_rating, '.2f'),
             'product_code': product_code, 'product_url': self.product_url}, indent=4)


def product(url: str):
    return Product(url).fetch_data()
