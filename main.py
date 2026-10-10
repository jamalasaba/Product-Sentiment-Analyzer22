import requests

# API address
url = "https://fakestoreapi.com/products"

# Request the product data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:

    products = response.json()

    print("PRODUCT DATA")
    print("=" * 40)

    for product in products:
        print("Product:", product["title"])
        print("Price: $", product["price"])
        print("Category:", product["category"])
        print("Rating:", product["rating"]["rate"])
        print("-" * 40)

else:
    print("Failed to fetch product data")