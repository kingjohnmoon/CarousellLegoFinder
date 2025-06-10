# CarousellLegoFinder
Attempts to compare prices of Lego sets between Carousell and Bricklink to find good deals

firstattempt.py contains the first attempt at the project simply by using the requests package.

It is based on the following article https://medium.com/@munkiat/automating-my-search-for-a-nintendo-switch-on-carousell-f94658f67b38 by Mun Kiat. Unfortunately, Carousell has disabled this method.

carousellscraper.py is my second version and works, utilising Selenium to get the name of the listing as well as its price (in SGD)

Do note that it currently only finds listings marked as 'Brand new', as used Lego sets can vary wildly in price based on which pieces they are missing, and so I don't wish to select for them.
