import re
import requests
import json
from carousellscraper import CarousellScraper

class BrickLinkComparer:

    def __init__(self, products):
        # Initialize the comparer with a list of products, a dictionary with title and price as keys.
        self.products = products

    def clean_products(self):
        # Clean the product titles and prices, and extract code from title.
        for product in self.products:
            product['title'] = product['title'].strip().lower()
            product['price'] = float(product['price'].replace('S$', '').replace(',', '').strip())
            # Extract the first number code (at least 3 digits) from the title
            match = re.search(r'\b(\d{3,})\b', product['title'])
            product['code'] = match.group(1) if match else None
        return self.products
    
    def get_brickset_info(self, api_key, codes):

        url = "https://brickset.com/api/v3.asmx/getSets"
        results = []
        for code in codes:
            params = {
                "setNumber": code
            }
            data = {
                "apiKey": api_key,
                "userHash": "",  # Leave blank if not using user authentication
                "params": json.dumps(params)
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            response = requests.post(url, data=data, headers=headers)
            # The response is XML, so you may want to parse it, but for now just append the text
            results.append({"setNumber": code, "response": response.text})
        return results
    

if __name__ == "__main__":
    products = CarousellScraper(5).run("lego")
    comparer = BrickLinkComparer(products)

    # cleaned_products = comparer.clean_products()
    # for product in cleaned_products:
    #     print(product)

    api_key = "3-fPfm-whNi-xl9Mc"  # Replace with your actual Brickset API key
    codes = ["42196"]
    brickset_infos = comparer.get_brickset_info(api_key, codes)
    for info in brickset_infos:
        print(f"Set Number: {info['setNumber']}")
        print(f"Response: {info['response']}")  # Print first 500 chars for brevity