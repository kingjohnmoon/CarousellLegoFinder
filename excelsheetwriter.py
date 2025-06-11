import openpyxl
from openpyxl.utils import get_column_letter
from carousellscraper import CarousellScraper
from bricklinkcomparer import BrickLinkComparer

class ExcelSheetWriter:
    def __init__(self, products, filename="lego_comparison.xlsx"):
        self.products = products
        self.filename = filename

    def write_to_excel(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Lego Comparison"
        # Write header
        headers = ["Title", "Carousell Price", "Set Code", "BrickLink Price"]
        ws.append(headers)
        # Write product rows
        for product in self.products:
            ws.append([
                product.get("title", ""),
                product.get("price", 0.0),  # price is now a float
                product.get("code", ""),
                product.get("bricklink_price", 0.0)  # bricklink_price is now a float
            ])
        # Auto-size columns
        for col in ws.columns:
            max_length = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except Exception:
                    pass
            ws.column_dimensions[col_letter].width = max_length + 2
        wb.save(self.filename)
        print(f"Excel file saved as {self.filename}")


if __name__ == "__main__":
    # Scrape products from Carousell
    scraper = CarousellScraper(0)  # Set the number of 'Brand new' listings to scrape here
    products = scraper.run("lego")
    
    # Compare with BrickLink prices
    comparer = BrickLinkComparer(products)
    cleaned_products = comparer.clean_products()
    price_info = comparer.get_price_info()
    filtered_products = comparer.filter_products_with_code_and_price()
    
    # Write to Excel
    writer = ExcelSheetWriter(filtered_products)
    writer.write_to_excel()