import re
from carousellscraper import CarousellScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrickLinkComparer:

    def __init__(self, products):
        # Initialize the comparer with a list of products, a dictionary with title and price as keys.
        self.products = products

    def clean_products(self):
        # Clean the product titles, and extract code from title.
        for product in self.products:
            product['title'] = product['title'].strip().lower()
            # Extract the first number code (at least 3 digits) from the title
            match = re.search(r'\b(\d{3,})\b', product['title'])
            product['code'] = match.group(1) if match else None
        return self.products
    
    def get_price_info(self):
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 15)
        # Go to Bricklink homepage to clear cookie popup once
        driver.get("https://www.bricklink.com/")
        try:
            cookie_buttons = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.cookie-notice__btn"))
            )
            for btn in cookie_buttons:
                if btn.text.strip().lower() == "just necessary":
                    btn.click()
                    break
        except Exception:
            pass  # Cookie button did not appear
        # Now iterate through products
        for product in self.products:
            code = product.get('code')
            if not code:
                product['bricklink_price'] = None
                continue
            url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?S={code}#T=P"
            driver.get(url)
            try:
                # Wait for the main price row to appear
                price_row = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "tr[style*='background-color: #C0C0C0']"))
                )
                # Find the first td in that row
                first_td = price_row.find_element(By.CSS_SELECTOR, "td")
                # Find the first summary table inside that td
                summary_table = first_td.find_element(By.CSS_SELECTOR, "table.pcipgSummaryTable")
                # Get the 4th row, 2nd column <b> (Avg Price)
                avg_price_cell = summary_table.find_element(By.CSS_SELECTOR, "tr:nth-child(4) td:nth-child(2) b")
                price_text = avg_price_cell.text.strip()
                # Convert BrickLink price to float (remove currency symbols, commas, etc.)
                try:
                    price_float = float(re.sub(r'[^\d.]', '', price_text))
                except Exception:
                    price_float = None
                product['bricklink_price'] = price_float
            except Exception:
                product['bricklink_price'] = None
        driver.quit()
        return self.products

    def filter_products_with_code_and_price(self):
        # Return only products with both a code and a bricklink price
        return [p for p in self.products if p.get('code') and p.get('bricklink_price')]

if __name__ == "__main__":
    products = CarousellScraper(5).run("lego")
    comparer = BrickLinkComparer(products)

    cleaned_products = comparer.clean_products()
    price_info = comparer.get_price_info()
    filtered_products = comparer.filter_products_with_code_and_price()
    for product in filtered_products:
        print(f"Title: {product['title']}, Price: {product['price']}, BrickLink Price: {product.get('bricklink_price', 'N/A')}")




