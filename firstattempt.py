# import requests
# import json

# class CarousellSearch(object):
#     def __init__(self, query_string=None, results=30):
#         self.base_url = ("https://carousell.com/ui/iso/api-main;path=/2.5/products/;query=")
#         self.fields = {
#             "count": results,
#             "sort": 'recent',
#             "query": query_string,
#             "lattitude": '',
#             "longitdue": '',
#             "lte": '',
#             "unit": '',
#             "country_id": '1880251',
#             "country_code": "SG"
#         }
#         query_fields = json.dumps(self.fields)
#         self.query_url = self.base_url + query_fields

#     def send_request(self):
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#             'Accept': 'application/json, text/plain, */*',
#         }
#         r = requests.get(self.query_url, headers=headers)
#         if r.status_code != 200:
#             print(f"HTTP Error: {r.status_code}\nResponse: {r.text}")
#             return []
#         try:
#             data = json.loads(r.text)
#         except json.JSONDecodeError as e:
#             print(f"JSON decode error: {e}\nResponse: {r.text}")
#             return []
#         return data.get('products', [])


# def find_stuff(search_query):
#     my_want = CarousellSearch(search_query, results=RESULTS_COUNT)
#     results = my_want.send_request()

#     for r in results:
#         #only keep results with my search
#         if search_query not in (r['title']).lower():
#             continue
#         #check if listing is in DB already
#         check = (session.query(CarousellListing).filter_by(listing_id=r['id']).
#                     first())
#         #if it is not in DB
#         if check is None:
#             listing = CarousellListing(
#                 listing_id = r['id'],
#                 seller = r['seller']['username'],
#                 title = r['title'],
#                 currency_symbol = r['currency_symbol'],
#                 price = r['price'],
#                 time = arrow.get(r['time_created']).format('DD/MM/YYYY HH:MM')
#             )
#             session.add(listing)
#             session.commit()
#             line_item = (r['seller']['username'], r['title'], r['price'],
#                         arrow.get(r['time_indexed']).format('DD/MM/YYYY HH:MM'))
#             robot.post_message(', '.join(line_item))
#     return


# if __name__ == "__main__":
#     search = CarousellSearch("lego", results=30)
#     results = search.send_request()
#     for item in results:
#         print(f"Title: {item['title']}, Price: {item['price']}, Seller: {item['seller']['username']}")


