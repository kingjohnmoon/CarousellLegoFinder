from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CarousellLegoScraper:
    def __init__(self, num_pages=1):
        self.num_pages = num_pages
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)

    def open_carousell(self):
        self.driver.get("https://www.carousell.sg/")
        time.sleep(3)

    # This method searches for a given query on Carousell
    # and waits for the results to load.
    def search(self, query):
        search_box = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search for an item']")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid^='listing-card-']")))

    # This method closes any pop-up that appears on the page.
    def close_popup(self):
        try:
            close_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.D_rT.D_arh[aria-label='Close']"))
            )
            close_btn.click()
            time.sleep(0.5)
        except Exception:
            pass

    # This method loads more results by clicking the "Show more results" button
    # until the specified number of pages is reached or no more results can be loaded.
    def load_more_results(self):
        listing_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid^='listing-card-']")
        for i in range(self.num_pages):
            try:
                show_more_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Show more results']"))
                )
                old_count = len(listing_cards)
                show_more_btn.click()
                self.wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "div[data-testid^='listing-card-']")) > old_count)
                listing_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid^='listing-card-']")
            except Exception as e:
                print(f"No more pages or could not load next page at iteration {i+1}:", e)
                break
        return listing_cards

    # This method scrapes the 'Brand new' listings from the provided listing cards.
    # Do note that the CSS Selectors used here are specific to the Dark Mode of Carousell.
    # It may need adjustments if you are using a different theme or if the website structure changes.
    def scrape_brand_new(self, listing_cards):
        results = []
        for card in listing_cards:
            try:
                card.find_element(By.XPATH, ".//p[normalize-space(text())='Brand new']")
            except:
                continue
            try:
                img = card.find_element(By.CSS_SELECTOR, "img.D_kC.D_XJ")
                title = img.get_attribute("alt")
            except:
                title = "N/A"
            try:
                price = card.find_element(By.CSS_SELECTOR, "div.D_qN p").text.strip()
            except:
                price = "N/A"
            results.append({"title": title, "price": price})
        return results

    def run(self, query="lego"):
        self.open_carousell()
        self.search(query)
        self.close_popup()
        listing_cards = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid^='listing-card-']")
        listing_cards = self.load_more_results()
        results = self.scrape_brand_new(listing_cards)
        # Optionally print or process results here
        self.driver.quit()
        return results

# Example usage:
if __name__ == "__main__":
    scraper = CarousellLegoScraper(5)  # Set the number of 'Brand new' listings to scrape here
    results = scraper.run()
    for item in results:
        print(f"Title: {item['title']}, Price: {item['price']}")

