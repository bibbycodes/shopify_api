import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("API_KEY")
api_pass = os.getenv("API_PASS")

class ShopifyApiParser:
  def __init__(self, api_key, api_pass):
    self.api_key = api_key
    self.api_pass = api_pass
    self.base_url = "https://{}:{}@themoflo.myshopify.com/admin/api/2019-10/{}.json"

  def parse_all_orders(self, array_of_orders):
    parsed_orders = []
    for order in array_of_orders:
      parsed_orders.append(self.parse_order(order))

    return parsed_orders


  def fetch_endpoint(self, endpoint):
    url = self.base_url.format(self.api_key, self.api_pass, endpoint)
    orders_request = requests.get(url)
    orders_json = json.loads(orders_request.text)
    array_of_orders = orders_json["orders"]

    return array_of_orders

  def parse_order(self, order):

    line_items = order["line_items"][0]
    parsed = {
      "order_id": order["id"],
      "email" : order["email"],
      "phone_number" : order["phone"],
      "created_at" : order["created_at"],
      "updated_at" : order["updated_at"],
      "processed_at" : order["processed_at"],
      "order_number" : order["order_number"],
      "total_price" : order["total_price"],
      "taxes_included" : order["taxes_included"],
      "quantity" : line_items["quantity"],
      "confirmed" : order["confirmed"],
      "checkout_token" : order["checkout_token"],
      "vendor" : line_items["title"],
      "ticket_type" : line_items["variant_title"],
      "address" : line_items["origin_location"],
      "billing_details" : order["billing_address"],
      "client_details" : order["client_details"],
      "fulfillment_status" : order["fulfillment_status"],
      }

    if ("payment_details" in order):
      parsed["payment_details"] = order["payment_details"]

    return parsed

MoFLo = ShopifyApiParser(api_key, api_pass)
unparserd_orders = MoFLo.fetch_endpoint("orders")
parsed_orders = MoFLo.parse_all_orders(unparserd_orders)

for order in parsed_orders:
  print(order)
  print("\n")