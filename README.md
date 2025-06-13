# CarousellLegoFinder
Attempts to compare prices of Lego sets between Carousell and Bricklink to find good deals

Requires Selenium and openpyxl

# First Attempt
firstattempt.py contains the first attempt at the project simply by using the requests package.

It is based on the following article https://medium.com/@munkiat/automating-my-search-for-a-nintendo-switch-on-carousell-f94658f67b38 by Mun Kiat. Unfortunately, Carousell has disabled this method.

# Carousell Scraper
carousellscraper.py is my second version and works, utilising Selenium to get the name of the listing as well as its price (in SGD)

Do note that it currently only finds listings marked as 'Brand new', as used Lego sets can vary wildly in price based on which pieces they are missing, and so I don't wish to select for them.

The scraper runs on Carousell dark mode on my PC, but should also work on light mode as I try to select elements not by colour

Users can input the number of extra pages it wants the scraper to check (0 for 1 extra page, 1 for 2, etc.)

It returns a list of dictionary objects that contains the title of the listing and a float that is the SGD price of listing

# Bricklink Comparer
brinklinkcomparer.py contains a class that takes in a list of products in the same format outputted by Carousell Scraper and checks Bricklink for their sale history, recording down the average sale price in the last 6 months.

Originally wanted to use Bricklink API but it requires a good review score on their page, which I don't have. So I used Selenium again. 

It returns a list of dictionary objects that contains the title of the listing, a float that is the SGD price of listing, and another float that is the Bricklink price

# Excel Sheetwriter
excelsheetwriter.py contains a class that takes in the output of Bricklink Comparer and writes results to an Excel file, with the following colour convention:

Red for listings with price higher than Bricklink price
Yellow for listings with price less than Bricklink price, but not more than 50SGD less
Green for listings with price less than Bricklink price by more than 50SGD

Do comment if you find any bugs or anything in my code, will try to take a look. Feel free to use it for your own projects.
